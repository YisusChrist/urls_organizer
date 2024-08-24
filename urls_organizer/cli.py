"""Command-line interface for the project."""

import sys
from argparse import ArgumentParser, ArgumentTypeError, Namespace

import pyfiglet  # pip install pyfiglet
import requests  # pip install requests
from rich import print  # pip install rich
from rich_argparse_plus import RichHelpFormatterPlus  # pip install rich-argparse-plus

from .consts import EXIT_FAILURE, GITHUB, LOG_PATH, PACKAGE
from .consts import __desc__ as DESC
from .consts import __version__ as VERSION
from .logs import logger

parser: ArgumentParser


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

    f = pyfiglet.Figlet(font="slant", justify="center", width=80)

    title_str: str = PACKAGE.replace("_", " ").capitalize()
    title: str = f"[green]{f.renderText(title_str)}"
    version: str = f"[i][red]Version: {VERSION}"
    desc: str = (
        f"[blue]{pyfiglet.figlet_format(f'{DESC} - {version}', font='term', justify='center')}"
    )
    repo: str = f"[cyan]{pyfiglet.figlet_format(GITHUB, font='term',justify='center')}"
    RichHelpFormatterPlus.choose_theme("prince")

    parser = ArgumentParser(
        description=f"{title}{desc}{repo}",  # Program description
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
        version=f"[argparse.prog]{PACKAGE}[/] version [i]{VERSION}[/]",
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
    sys.exit(exit_value)


def check_updates() -> None:
    """
    Check if there is a newer version of the script available in the GitHub repository.
    """
    project: str = GITHUB.split("https://github.com/")[1]
    repo_url: str = f"https://api.github.com/repos/{project}/releases/latest"

    try:
        response: requests.Response = requests.get(repo_url, timeout=5)
        response.raise_for_status()

        latest_version: str = response.json()["tag_name"]
        if latest_version != VERSION:
            logger.warning(
                "\n[yellow]Newer version of the script available: "
                f"{latest_version}.\nPlease consider updating your version.[/]"
            )

    except requests.exceptions.RequestException:
        logger.error("Could not check for updates")


def print_help():
    """
    Print the help message.
    """
    global parser

    parser.print_help()
