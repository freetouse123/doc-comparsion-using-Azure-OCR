"""
Function execution time decorator
"""

import time
from functools import wraps
from config.config import DefaultConfig

logger = DefaultConfig().logger

def time_decorator(func):
    """
    Decorator to measure execution time of a function.
    Works for class methods or standalone functions.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logger.info(f"Time taken to execute '{func.__name__}' = {end_time - start_time:.4f} seconds")
            return result
        except Exception as e:
            logger.info(f"Error while executing '{func.__name__}': {e}")
            raise
    return wrapper

