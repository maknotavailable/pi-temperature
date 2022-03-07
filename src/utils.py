from datetime import datetime, timedelta
import os
from pathlib import Path
import configparser
import logging
import traceback


class Logger:
    def __init__(self, source_name: str = None) -> None:
        if source_name is None:
            source_name = __name__
        self.log = logging.getLogger(source_name)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        )

    def info(self, message: str):
        self.log.info(message)

    def warning(self, message: str):
        self.log.warning(message)

    def error(self, message: str, incl_traceback: bool = False):
        self.log.error(message)
        if incl_traceback:
            traceback.print_exc()


log = Logger(__name__)


def get_repo_dir():
    """Get repository root directory"""
    root_dir = "./"
    if os.path.isdir(Path(__file__).parent.parent / "src"):
        root_dir = f"{(Path(__file__).parent.parent).resolve()}/"
    elif os.path.isdir("../../src"):
        root_dir = "../../"
    elif os.path.isdir("../src"):
        root_dir = "../"
    elif os.path.isdir("./src"):
        root_dir = "./"
    else:
        log.warning(
            "Root repository directory not found. This may "
            "be an issue when trying to load from /assets or "
            "the local config.ini."
        )
    return root_dir


def get_config(section=None):
    """Load local config file"""
    run_config = configparser.ConfigParser()
    run_config.read(get_repo_dir() + "config.ini")
    if len(run_config) == 1:
        run_config = None
    elif section is not None:
        run_config = run_config[section]
    return run_config


def get_secret(name, section="env", is_required: bool = True):
    config = get_config(section=section)
    value = None

    if config is not None and name in config:
        # Get secret from local config
        value = config[name]
    elif name in os.environ:
        # Get secret from environment variable
        value = os.environ[name]

    if value is None and is_required:
        raise KeyError(f"The secret {name} was not found.")

    return value


def time_difference_passed_threshold(
    time1: datetime, time2: datetime, difference: int
) -> bool:
    if (time1 - time2) > timedelta(minutes=difference):
        return True
    else:
        return False
