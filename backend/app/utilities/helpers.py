import os


def is_dev() -> bool:
    """Check if the current environment is development"""
    return os.getenv("ENV") == "development"


def is_prod() -> bool:
    """Check if the current environment is production"""
    return os.getenv("ENV") == "production"


def is_valid_environment() -> bool:
    """Check if the current environment is valid"""
    return is_dev() or is_prod()
