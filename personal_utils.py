#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@file     utils.py
@date     2023-02-01
@version  1.0
@license  GNU General Public License v3.0
@url      https://github.com/yisuschrist/urls_organizer
@author   Alejandro Gonzalez Momblan (agelrenorenardo@gmail.com)
@desc     Collection of utility functions.

@details  This file contains a collection of utility functions that are used
          throughout the project. These functions are not specific to any
          particular module and are used by multiple modules.

@note     This file is part of the urls_organizer project.
            
@requires Python 3.6 or greater
          termcolor
          prettytable
"""
import os
import subprocess
from typing import List

from termcolor import cprint  # pip install termcolor
from prettytable import PrettyTable  # pip install prettytable


# ANSI escape codes for text colors
COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "light_grey": "\033[90m",
    "dark_grey": "\033[90m",
    "light_red": "\033[91m",
    "light_green": "\033[92m",
    "light_yellow": "\033[93m",
    "light_blue": "\033[94m",
    "light_magenta": "\033[95m",
    "light_cyan": "\033[96m",
}

# ANSI escape codes for text highlights
HIGHLIGHTS = {
    "on_black": "\033[40m",
    "on_red": "\033[41m",
    "on_green": "\033[42m",
    "on_yellow": "\033[43m",
    "on_blue": "\033[44m",
    "on_magenta": "\033[45m",
    "on_cyan": "\033[46m",
    "on_white": "\033[47m",
    "on_light_grey": "\033[100m",
    "on_dark_grey": "\033[100m",
    "on_light_red": "\033[101m",
    "on_light_green": "\033[102m",
    "on_light_yellow": "\033[103m",
    "on_light_blue": "\033[104m",
    "on_light_magenta": "\033[105m",
    "on_light_cyan": "\033[106m",
}

# ANSI escape codes for text attributes
ATTRIBUTES = {
    "bold": "\033[1m",
    "dark": "\033[2m",
    "underline": "\033[4m",
    "blink": "\033[5m",
    "reverse": "\033[7m",
    "concealed": "\033[8m",
}

# ANSI escape code to reset all attributes
RESET = "\033[0m"

# ANSI escape code to clear the screen
CLEAR = "\033[2J\033[H"


print_colored = lambda text, color: cprint(text, color)


print_list_with_commas = lambda l: print(", ".join(l)) if l else None


def grab(text: str, start: str, end: str = "\n") -> str:
    """
    Extract a string between a given start and end string within a larger string.

    Args:
        text (str): The larger string to search within.
        start (str): The starting string to search for.
        end (str, optional): The ending string to search for. Defaults to "\n".

    Returns:
        str: The string between the start and end strings, if found. Otherwise, an empty string.

    """
    # Find the starting index of the desired substring
    start_index = text.find(start)
    # Find the ending index of the desired substring
    end_index = text.find(end, start_index + len(start))
    # Return the substring between the start and end indices.
    return text[start_index + len(start) : end_index]


def ensure_exists(*paths: str) -> None:
    """
    Check whether the specified directories or files exist and create them if
    they do not.

    Args:
        *dirs: str: The directories or files to check/create.
    """
    for path in paths:
        if not os.path.exists(path):
            if os.path.isdir(path):
                os.makedirs(path)
            else:
                open(path, "a").close()


def remove_duplicates(l: list) -> list:
    """
    Remove duplicate elements from a given list.

    Args:
        l (list): The list to remove duplicates from.

    Returns:
        list: The input list with duplicates removed.
    """
    return list(set(l))


def run_cmd(cmd) -> str:
    """
    Run a command and return the output

    Args:
        cmd (str): Command to run

    Returns:
        str: Output of the command

    Raises:
        CalledProcessError: If the command returns a non-zero exit status

    Notes:
        This function is used to run commands in the terminal
        and return the output of the command

        This function is used to run commands that are not
        available in the Python standard library or that require
        the use of the shell

        For example, the "cp" command is not available in the
        Python standard library and requires the use of the shell
        to copy directories and files, so it is necessary to use this
        function to run the command
    """
    try:
        output = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError:
        output = ""
    return output.decode("utf-8").strip()


def run_shell_command(
    cmd: str, verbose: bool = False, *args, **kwargs
) -> None:
    """
    Run a command in the shell and print the output.

    Args:
        cmd (str): The command to run.
        verbose (bool): Whether to print the output of the command to the
            console.
        *args: Additional positional arguments to be passed to
            `subprocess.Popen`.
        **kwargs: Additional keyword arguments to be passed to
            `subprocess.Popen`.
    """
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        shell=True,
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)


def get_file_extension(file_path: str) -> str:
    """
    Get the extension of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The extension of the file.
    """
    return os.path.splitext(file_path)[1]


def get_file_name(file_path: str) -> str:
    """
    Get the name of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The name of the file.
    """
    return os.path.splitext(os.path.basename(file_path))[0]


def get_file_size(file_path: str) -> int:
    """
    Get the size of a file in bytes.

    Args:
        file_path (str): The path to the file.

    Returns:
        int: The size of the file in bytes.
    """
    return os.path.getsize(file_path)


def read_file(file_path: str) -> str:
    """
    Read the contents of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The contents of the file.

    Raises:
        FileNotFoundError: If the specified file cannot be found.
    """
    try:
        # Open the file with utf-8 encoding and return the contents
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")


def write_file(file_path: str, content: str) -> None:
    """
    Write a string to a file.

    Args:
        file_path (str): The path to the file.
        content (str): The string to write to the file.

    Raises:
        FileNotFoundError: If the specified file cannot be found.
    """
    try:
        # Open the file with utf-8 encoding and save the content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found")


def flatten(l: list) -> list:
    """
    Flatten a list of lists.

    Args:
        l (list): The list to flatten.

    Returns:
        list: The flattened list.
    """
    return [item for sublist in l for item in sublist]


def split_by_n(s: str, n: int) -> list:
    """
    Split a string into a list of n-length substrings.

    Args:
        s (str): The string to split.
        n (int): The length of each substring.

    Returns:
        list: A list of n-length substrings.
    """
    return [s[i : i + n] for i in range(0, len(s), n)]


def merge_dicts(*dicts: dict) -> dict:
    """
    Merge any number of dictionaries into a single dictionary.

    Args:
        *dicts: The dictionaries to merge.

    Returns:
        dict: The merged dictionary.
    """
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged


def print_table(data: List[List[str]], headers: List[str] = []) -> None:
    """
    Prints a table of data using the prettytable module.

    Args:
        data (List[List[str]]): A list of rows, where each row is a list of
            strings representing the columns.
        headers (List[str]): A list of header strings for the table. Optional.

    Returns:
        None
    """
    table = PrettyTable()
    if headers:
        table.field_names = headers
    for row in data:
        table.add_row(row)
    print(table)
