"""Utility functions used throughout the project."""

from pathlib import Path


def ensure_exists(*paths: str) -> None:
    """
    Check whether the specified directories or files exist and create them if
    they do not.

    Args:
        *paths: str: The directories or files to check/create.
    """
    for path in paths:
        if "." in path:  # argument is a file
            real_path = Path(path).resolve()
            # Create the directory if it does not exist
            Path(real_path).parent.mkdir(parents=True, exist_ok=True)
            # Create the file if it does not exist
            Path(real_path).touch()
        else:  # argument is a directory
            # Create the directory if it does not exist
            Path(path).mkdir(parents=True)
