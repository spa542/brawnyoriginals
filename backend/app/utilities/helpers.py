import os
from configparser import ConfigParser
from pathlib import Path


def is_dev() -> bool:
    """Check if the current environment is development"""
    return os.getenv("ENV") == "development"


def is_prod() -> bool:
    """Check if the current environment is production"""
    return os.getenv("ENV") == "production"


def is_valid_environment() -> bool:
    """Check if the current environment is valid"""
    return is_dev() or is_prod()


def get_cfg_name() -> str:
    """Get the configuration name"""
    return "dev" if is_dev() else "prod" 


def get_cfg() -> ConfigParser:
    """Get the configuration parser"""
    cfg = ConfigParser()
    # Get the directory where this file is located
    current_dir = Path(__file__).parent
    # Navigate to the conf directory and read the config file
    config_path = current_dir.parent / "conf" / f"{get_cfg_name()}.ini"
    cfg.read(config_path)
    return cfg