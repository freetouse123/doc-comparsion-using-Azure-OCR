# logger.py
import logging
import sys
from datetime import datetime
from pathlib import Path

class Logger:
    """Simple logger with basic info, warning, and error capabilities"""
    
    def __init__(self, name="SalesAgent", log_to_file=False, log_file="app.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers = []
        
        # Create formatters
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler (with colors)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File Handler (optional)
        if log_to_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(f"{message}")
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(f" {message}")
    
    def error(self, message, exception=None):
        """Log error message"""
        if exception:
            self.logger.error(f" {message}: {str(exception)}", exc_info=True)
        else:
            self.logger.error(f" {message}")
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(f" {message}")
    
    def success(self, message):
        """Log success message (as info level)"""
        self.logger.info(f" {message}")

