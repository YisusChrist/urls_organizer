"""Constants for the project."""

import os
from pathlib import Path

from platformdirs import user_config_dir, user_log_dir, user_data_dir, user_cache_dir

try:
    from importlib import metadata
except ImportError:  # for Python < 3.8
    import importlib_metadata as metadata

__version__ = metadata.version(__package__ or __name__)
__desc__ = metadata.metadata(__package__ or __name__)["Summary"]
PACKAGE = metadata.metadata(__package__ or __name__)["Name"]
GITHUB = metadata.metadata(__package__ or __name__)["Home-page"]

CACHE_PATH = user_cache_dir(appname=PACKAGE, ensure_exists=True)
CONFIG_PATH = user_config_dir(appname=PACKAGE, ensure_exists=True)
CONFIG_FILE = Path(CONFIG_PATH).resolve() / f"{PACKAGE}.ini"
DATA_PATH = user_data_dir(appname=PACKAGE, ensure_exists=True)
LOG_PATH = user_log_dir(appname=PACKAGE, ensure_exists=True)
LOG_FILE = Path(LOG_PATH).resolve() / f"{PACKAGE}.log"

MULTIPROCESSING_THREADS: int = os.cpu_count() * 2
INVALID_URLS_FILE = "invalid_urls_tmp.txt"
MAX_TIMEOUT = 10

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

DEBUG = False
PROFILE = False
