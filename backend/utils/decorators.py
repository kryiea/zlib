import functools
import time
from typing import Any, Callable
from functools import lru_cache
from config import Config

def retry_on_failure(max_retries: int = 3, delay: float = 1.0) -> Callable:
    """
    Retry decorator for failed requests
    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_error = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            raise last_error
        return wrapper
    return decorator

def cache_response(timeout: int = Config.CACHE_TIMEOUT) -> Callable:
    """
    Cache decorator for responses
    Args:
        timeout: Cache timeout in seconds
    """
    def decorator(func: Callable) -> Callable:
        # Only enable cache if configured
        if not Config.ENABLE_CACHE:
            return func
            
        @lru_cache(maxsize=128)
        def cached_func(*args, **kwargs) -> Any:
            return func(*args, **kwargs)
            
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return cached_func(*args, **kwargs)
            
        return wrapper
    return decorator 