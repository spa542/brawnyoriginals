import os
from configparser import ConfigParser


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
    # TODO make sure this path works anywhere 
    cfg.read(f"app/conf/{get_cfg_name()}.ini")
    return cfg