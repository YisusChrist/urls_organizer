#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
@file     __main__.py
@date     2023-11-26
@version  1.1 (Stable)
@license  GNU General Public License v3.0
@url      https://github.com/yisuschrist/urls_organizer
@author   Alejandro Gonzalez Momblan (agelrenorenardo@gmail.com)

@todo     - Add support for arguments completion with argcomplete.
            Reference: https://pypi.org/project/argcomplete/#global-completion
          - Generate HTML documentation with Sphinx/PDoc.
            Reference: https://realpython.com/documenting-python-code/
          - Use linter to check code style.
"""
from rich import print  # pip install rich
from rich.traceback import install  # pip install rich

from .cli import check_updates, exit_session, get_parsed_args, print_help
from .consts import (DEBUG, EXIT_FAILURE, EXIT_SUCCESS, INVALID_URLS_FILE,
                     PROFILE)
from .logs import logger
from .personal_utils import ensure_exists
from .urls import (get_invalid_urls, get_urls_from_file, merge_content,
                   parse_url, save_urls_to_file, validate_url_list)


def main():
    """
    Main function of the script.
    """
    args = get_parsed_args()
    logger.info("Starting session...")

    check_updates()

    if not (args.saveFile and (args.readFile or args.url)):
        print("[red]ERROR: No destination file or source file/URL specified[/]")
        print_help()
        exit_session(EXIT_FAILURE)

    ensure_exists(INVALID_URLS_FILE, args.saveFile)

    if args.readFile:
        # Read URLs from file
        data = get_urls_from_file(args.readFile)
    else:
        # Read URL from command line
        data = [parse_url(args.url)]
        logger.debug(f"The new URL is {data[0]}")

    old_length = len(data)

    # Merge data
    data = merge_content(data, args.saveFile)

    new_length = len(data)

    if args.numWorkers > 0:
        validate_url_list(args, data)

    # Save the final collection URLs to file
    invalid_url_list = get_invalid_urls()
    if invalid_url_list:
        logger.info(f"Invalid URLs found! Check the file {INVALID_URLS_FILE}")

        invalid_url_list = merge_content(invalid_url_list, INVALID_URLS_FILE)
        # Save the invalid URLs to file
        save_urls_to_file(invalid_url_list, INVALID_URLS_FILE)

        data = [u for u in data if u not in invalid_url_list]

    # Save the final collection URLs to file
    save_urls_to_file(data, args.saveFile)

    print("\nOperation finished!\n")
    logger.info(
        f"Found {old_length - new_length} duplicate URLs out of "
        f"{old_length} total URLs"
        if old_length > new_length
        else "No duplicate URLs found"
    )

    exit_session(EXIT_SUCCESS)


if __name__ == "__main__":
    # Enable rich error formatting in debug mode
    install(show_locals=DEBUG)
    if DEBUG:
        print("[yellow]Debug mode is enabled[/yellow]")
    if PROFILE:
        import cProfile

        print("[yellow]Profiling is enabled[/yellow]")
        cProfile.run("main()")
    else:
        main()
