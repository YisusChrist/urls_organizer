import hashlib
import os
import signal
from argparse import Namespace
from functools import lru_cache
from multiprocessing import Manager, Pool

import requests  # pip install requests
import validators  # pip install validators
from natsort import natsorted  # pip install natsort
from tqdm import tqdm  # pip install tqdm

from .cli import exit_session
from .consts import (CACHE_PATH, EXIT_FAILURE, MAX_TIMEOUT,
                     MULTIPROCESSING_THREADS)
from .logs import logger

manager = Manager()
invalid_url_list = manager.list()


def init_worker() -> None:
    """
    Initialize the worker process.

    This function sets the signal handling for the worker process to ignore
    the `SIGINT` signal.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def normalize_url(url: str) -> str:
    """
    Remove unnecessary URL extensions from a given string.

    Args:
        url (str): The string to remove the extensions from.

    Returns:
        str: The input string with unnecessary URL extensions removed.
    """
    # Can't remove / from end of URL because it is used to identify directories
    if url.endswith("#"):
        url = url[:-1]

    return (
        url.replace("/www.", "/")
        .replace("/m.", "/")
        .replace("/es.", "/")
        .replace("http:", "https:")
    )


def parse_url(url: str) -> str:
    """
    Parse a URL string and remove unnecessary parts.

    Args:
        url (str): The URL to parse.

    Returns:
        str: The parsed URL with unnecessary parts removed.
    """
    logger.debug("Parsing URL: %s" % url)

    # List of URL extensions to remove
    extension_rules = [
        "&",
        "?",
        "/?",
        "/#",
    ]
    keep_extension = "viewkey"

    # Remove whitespaces to avoid errors
    url = url.strip()

    # Remove URL additional media data
    if keep_extension not in url:
        for r in extension_rules:
            url = url.split(r, 1)[0]

    # Keep the ?viewkey parameter and remove other query parameters
    url_parts = url.split("?")
    if len(url_parts) > 1:
        base_url = url_parts[0]
        query_params = url_parts[1].split("&")
        keep_params = [p for p in query_params if p.startswith(keep_extension)]
        url = base_url + "?" + "&".join(keep_params)

    # Remove unnecessary URL extensions
    return normalize_url(url)


@lru_cache()
def validate_url(url: str) -> None:
    """
    Validate the given URL by making a GET request and checking the response status code.

    Args:
        url (str): The URL to validate.

    Raises:
        InvalidURL: If the URL is not valid.
    """
    #! TODO: Shared memory between processes does not work on Windows
    # Reference: https://stackoverflow.com/questions/40630428/share-a-list-between-different-processes
    global invalid_url_list

    logger.debug("Validating URL: <%s>" % url)

    # Remove the URL title if it exists
    url = url.split(" (")[0]

    # check if the link is in the cache
    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()
    filename = os.path.join(CACHE_PATH, url_hash)
    if os.path.exists(filename):
        logger.warning("Link %s already visited, skipping...", url)
        return

    # Make a GET request
    try:
        if not validators.url(url):
            logger.error("Invalid URL: %s" % url)
        else:
            #! TODO: Fix when some pages return code != 200 but the page is valid
            response = requests.get(url, timeout=MAX_TIMEOUT)
            response.raise_for_status()

            # save to cache
            cache_file = os.path.join(CACHE_PATH, url_hash)
            with open(cache_file, "w", encoding="utf-8"):
                pass

            return

    except requests.exceptions.HTTPError as e:
        logger.info("Invalid URL: %s with status code %s" % (url, response.status_code))
    except requests.exceptions.ConnectionError:
        logger.error("Error connecting to %s" % url)
    except OSError:
        logger.error("Error making GET request to %s" % url)
    except Exception as e:
        logger.exception(e)

    invalid_url_list.append(url)


def validate_url_list(args: Namespace, url_list: list):
    """
    Validate a list of URLs using multiple processes and display the number
    of invalid URLs found.

    Args:
        args (argparse.Namespace): Namespace object containing command-line
                                   arguments.
        url_list (list): List of URLs to be validated.
    """
    logger.debug("Validating URLs...")

    # Calculate optimal number of processes based on system capacity
    optimal_processes = min(MULTIPROCESSING_THREADS, len(url_list))
    num_processes = min(args.numWorkers, optimal_processes)
    if num_processes < args.numWorkers:
        logger.warning(
            f"Warning: numWorkers set to {args.numWorkers}, which is above "
            f"the optimal value of {MULTIPROCESSING_THREADS}. Using "
            f"{num_processes} workers instead."
        )

    try:
        with Pool(processes=num_processes, initializer=init_worker) as pool:
            for _ in tqdm(
                pool.imap_unordered(validate_url, url_list),
                total=len(url_list),
            ):
                pass
    except KeyboardInterrupt:
        logger.info("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
        pool.join()

    logger.info(f"Found {len(invalid_url_list)} invalid URLs out of {len(url_list)}")


def get_urls_from_file(file_path: str) -> list:
    """
    Read a file and return a list of URLs after parsing.

    Args:
        file (str): The path to the file to read.

    Returns:
        list: A list of URLs after parsing.
    """
    logger.debug("Reading URLs from file: %s" % file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
    except FileNotFoundError as e:
        # If the file is not found, log an error and exit the program with an error code
        logger.error(e)
        exit_session(EXIT_FAILURE)
    # Parse each line as a URL
    return [parse_url(line) for line in content]


def save_urls_to_file(url_list: list, file_path: str) -> None:
    """
    Save a list of URLs to a file.

    Args:
        url_list (list): The list of URLs to save.
        file_path (str): The path of the file to save to.
    """
    logger.debug("Saving URLs to file: %s" % file_path)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines("\n".join(url_list))
    except FileNotFoundError as e:
        # If the file is not found, log an error and exit the program with an error code
        logger.error(e)
        exit_session(EXIT_FAILURE)


def merge_content(data: list, file_path: str) -> list:
    """
    Merge a list of strings with the contents of a file, removing duplicates.

    Args:
        data (list): The list of strings to merge with the file.
        file_path (str): The path of the file to merge with.

    Returns:
        list: The merged list with duplicates removed.
    """
    logger.debug("Merging content from file: %s" % file_path)

    file_data = get_urls_from_file(file_path)
    # Remove duplicates from the merged data
    merged_data = list(set(data + file_data))
    # Sort the merged data in natural order
    return natsorted(merged_data)


def get_invalid_urls() -> list:
    """
    Return the list of invalid URLs.

    Returns:
        list: The list of invalid URLs.
    """
    global invalid_url_list
    return list(invalid_url_list)
