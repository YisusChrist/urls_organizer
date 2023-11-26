"""Constants for the project."""
import os
from pathlib import Path

from platformdirs import user_config_dir, user_log_dir, user_data_dir, user_cache_dir

from . import PACKAGE, __desc__, __version__

NAME = PACKAGE  # Path(__file__).name.split(".")[0]
CACHE_PATH = user_cache_dir(appname=NAME, ensure_exists=True)
CONFIG_PATH = user_config_dir(appname=NAME, ensure_exists=True)
CONFIG_FILE = Path(CONFIG_PATH).resolve() / f"{NAME}.ini"
DATA_PATH = user_data_dir(appname=NAME, ensure_exists=True)
LOG_PATH = user_log_dir(appname=NAME, ensure_exists=True)
LOG_FILE = Path(LOG_PATH).resolve() / f"{NAME}.log"
VERSION = __version__
DESC = __desc__

MULTIPROCESSING_THREADS = os.cpu_count() * 2
INVALID_URLS_FILE = "invalid_urls_tmp.txt"
MAX_TIMEOUT = 10

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

DEBUG = False
PROFILE = False
