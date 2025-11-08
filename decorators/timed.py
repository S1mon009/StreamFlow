"""
This module provides a decorator for measuring the execution time of functions.

Functions:
    timed: Decorator that measures and displays the execution time of the decorated function.
"""

import time

def timed(func:callable) -> callable:
    """Decorator that measures and displays the execution time of a function.

    The execution time is shown in seconds if less than 60 seconds, 
    otherwise in minutes.

    Args:
        func (Callable): Function to decorate.

    Returns:
        Callable: Wrapped function that measures execution time.
    """
    def wrapper(*args:tuple, **kwargs:dict[str, dict]) -> callable:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if elapsed_time < 60:
            print(f"\nDownload time: {elapsed_time:.2f} seconds.")
        else:
            print(f"\nDownload time: {elapsed_time / 60:.2f} minutes.")

        return result
    return wrapper
