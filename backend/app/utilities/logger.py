import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Any, Union


# Module-level variables
_initialized = False
_root_logger = None


def init_logger(
    log_level: int = logging.INFO,
    log_file: Optional[Union[str, Path]] = None,
    log_dir: str = 'logs'
) -> None:
    """
    Initialize the application logger.
    
    Args:
        log_level: Logging level (e.g., logging.INFO, logging.DEBUG)
        log_file: Path to the log file (relative to log_dir if not absolute)
        log_dir: Directory to store log files (if log_file is relative)
    """
    global _initialized, _root_logger
    
    if _initialized:
        return
        
    # Create logs directory if it doesn't exist
    log_dir_path = Path(log_dir) if os.path.isabs(log_dir) else Path(__file__).parent.parent / log_dir
    log_dir_path.mkdir(parents=True, exist_ok=True)
    
    # Determine log file path
    if log_file:
        log_file_path = Path(log_file)
        if not log_file_path.is_absolute():
            log_file_path = log_dir_path / log_file_path
    else:
        log_file_path = log_dir_path / 'app.log'
    
    # Create root logger
    logger = logging.getLogger('app')
    logger.setLevel(log_level)
    
    # Clear any existing handlers to avoid duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=5 * 1024 * 1024,  # 5MB per file
        backupCount=5,  # Keep 5 backup files
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    _root_logger = logger
    _initialized = True
    
    # Log initialization
    logger.info("Logger initialized")
    logger.info(f"Log level set to: {logging.getLevelName(log_level)}")
    logger.info(f"Log file: {log_file_path.absolute()}")


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Optional name for the logger. If not provided, returns the root logger.
             If provided, creates a child logger with the given name.
             
    Returns:
        Configured logger instance
        
    Raises:
        RuntimeError: If the logger has not been initialized
    """
    if not _initialized:
        raise RuntimeError(
            "Logger not initialized. Call init_logger() first."
        )
    
    if name:
        return logging.getLogger(f'app.{name}')
    return _root_logger


# Convenience functions that require initialization
def debug(msg: str, *args: Any, **kwargs: Any) -> None:
    if _initialized:
        _root_logger.debug(msg, *args, **kwargs)
    else:
        raise RuntimeError("Logger not initialized. Call init_logger() first.")


def info(msg: str, *args: Any, **kwargs: Any) -> None:
    if _initialized:
        _root_logger.info(msg, *args, **kwargs)
    else:
        raise RuntimeError("Logger not initialized. Call init_logger() first.")


def warning(msg: str, *args: Any, **kwargs: Any) -> None:
    if _initialized:
        _root_logger.warning(msg, *args, **kwargs)
    else:
        raise RuntimeError("Logger not initialized. Call init_logger() first.")


def error(msg: str, *args: Any, **kwargs: Any) -> None:
    kwargs.setdefault('exc_info', True)
    if _initialized:
        _root_logger.error(msg, *args, **kwargs)
    else:
        raise RuntimeError("Logger not initialized. Call init_logger() first.")


def critical(msg: str, *args: Any, **kwargs: Any) -> None:
    kwargs.setdefault('exc_info', True)
    if _initialized:
        _root_logger.critical(msg, *args, **kwargs)
    else:
        raise RuntimeError("Logger not initialized. Call init_logger() first.")
