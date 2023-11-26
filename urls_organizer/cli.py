"""Command-line interface for the project."""
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
from sys import exit

import pyfiglet  # pip install pyfiglet
import requests  # pip install requests
from rich import print  # pip install rich
from rich_argparse_plus import RichHelpFormatterPlus  # pip install rich-argparse-plus
from string_grab import grab  # pip install string-grab

from . import GITHUB
from .consts import DESC, EXIT_FAILURE, LOG_PATH, NAME, VERSION
from .logs import logger

parser = None


def check_positive(value: str) -> int:
    """
    Check if a given value is a positive integer and return it.

    Args:
        value (str): The value to check.

    Returns:
        int: The input value as an integer if it is a positive integer.

    Raises:
        argparse.ArgumentTypeError: If the input value is not a positive integer.
    """
    ivalue = int(value)
    if ivalue <= 0:
        raise ArgumentTypeError("%s is not a valid value" % value)
    return ivalue


def get_parsed_args() -> Namespace:
    """
    Parse and return command-line arguments.

    Returns:
        The parsed arguments as an Namespace object.
    """
    global parser

    title = NAME.replace("_", " ").capitalize()
    f = pyfiglet.Figlet(font="slant", justify="center", width=80)
    title = print(f"[green]{f.renderText(title)}[/]")
    desc = print(
        f"[cyan]{pyfiglet.figlet_format(DESC,font='term',justify='center',)}[/]"
    )
    RichHelpFormatterPlus.choose_theme("prince")

    parser = ArgumentParser(
        description=f"{title}{desc}",  # Program description
        formatter_class=RichHelpFormatterPlus,  # Custom help formatter
        allow_abbrev=False,  # Disable abbreviations
        add_help=False,  # Disable default help
    )

    g_targets = parser.add_argument_group("Options to add URLs")
    g_targets.add_argument(
        "-sf",
        "--saveFile",
        dest="saveFile",
        default=False,
        help="File with the URLs result. Argument is required",
        required=False,
    )
    g_targets.add_argument(
        "-rf",
        "--readFile",
        dest="readFile",
        default=False,
        help="File with the URLs to add. Argument is required if -u is not used.",
    )
    g_targets.add_argument(
        "-u",
        "--url",
        dest="url",
        default=False,
        help="Single URL to add. Argument is required if -rf is not used.",
    )
    g_targets.add_argument(
        "-w",
        "--numWorkers",
        dest="numWorkers",
        default=0,
        type=check_positive,
        help="Number of workers to use. Default is the number of CPU cores * 2.",
    )

    g_misc = parser.add_argument_group("Miscellaneous Options")
    # Help
    g_misc.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )
    # Verbose
    g_misc.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Show log messages on screen. Default is False.",
    )
    # Debug
    g_misc.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Activate debug logs. Default is False.",
    )
    g_misc.add_argument(
        "-V",
        "--version",
        action="version",
        help="Show version number and exit.",
        version=f"[argparse.prog]{NAME}[/] version [i]{VERSION}[/]",
    )

    return parser.parse_args()


def exit_session(exit_value: int) -> None:
    """
    Exit the program with the given exit value.

    Args:
        exit_value (int): The POSIX exit value to exit with.
    """
    logger.info("End of session")
    # Check if the exit_value is a valid POSIX exit value
    if not 0 <= exit_value <= 255:
        exit_value = EXIT_FAILURE

    if exit_value == EXIT_FAILURE:
        print(
            "\n[red]There were errors during the execution of the script. "
            f"Check the logs at '{LOG_PATH}' for more information.[/]"
        )

    # Exit the program with the given exit value
    exit(exit_value)


def extract_header_key(key: str, file: str) -> str:
    """
    Extract the value associated with the given key from the header.

    Args:
        key (str): The key to extract from the header.

    Returns:
        str: The value associated with the key.

    Raises:
        KeyError: If the key is not found in the header.
    """
    try:
        # Open the file and read its contents.
        with open(file) as f:
            content = f.read()
        # Extract the value associated with the key.
        return str(grab(content, start=f"@{key}", end="\n").strip())
    except LookupError:
        print(f"[red]Could not extract key '{key}' from header[/red]")
        exit_session(EXIT_FAILURE)


def check_updates():
    """
    Check if there is a newer version of the script available in the GitHub repository.

    Returns:
        str: A message indicating if there is a newer version available or not.
    """
    logger.debug("Checking for updates...")

    file = f"{NAME}/__main__.py"
    if not Path(file).exists():
        logger.error("Could not find the file '%s'" % file)
        return

    project = GITHUB.split("https://github.com/")[1]
    repo_url = f"https://api.github.com/repos/{project}/releases/latest"

    try:
        response = requests.get(repo_url)
        response.raise_for_status()
        latest_version = response.json()["tag_name"]
        if latest_version != VERSION:
            print(
                f"\n[yellow]Newer version of the script available: {latest_version}.\n"
                "Please consider updating your version.[/yellow]"
            )

            logger.warning("Newer version of the script available: %s" % latest_version)
        else:
            logger.info("You are using the latest version of the script")
    except requests.exceptions.RequestException:
        logger.error("Could not check for updates")


def print_help():
    """
    Print the help message.
    """
    global parser

    parser.print_help()
