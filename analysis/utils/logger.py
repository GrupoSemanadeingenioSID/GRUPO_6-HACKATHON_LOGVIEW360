"""
Logging configuration for the LogView360 analysis module.
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str, log_file: str = None, level=logging.INFO):
    """
    Set up a logger with console and file handlers.
    
    Args:
        name (str): Logger name
        log_file (str, optional): Path to log file. Defaults to None.
        level: Logging level. Defaults to logging.INFO.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler if log_file is specified
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create default logger
default_logger = setup_logger('logview360') 