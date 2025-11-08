"""
Module providing network-related utilities.

This module including:
- `is_connected()`: Check internet connectivity.
- `network_required`: Decorator that ensures a network connection before executing a function.
"""

import socket
import time

def is_connected(host:str="8.8.8.8", port:int=53, timeout:int=3) -> bool:
    """Check internet connectivity by attempting to connect to a public DNS server.

    Args:
        host (str, optional): Host to connect to. Defaults to "8.8.8.8" (Google DNS).
        port (int, optional): Port to use for the connection. Defaults to 53.
        timeout (int, optional): Connection timeout in seconds. Defaults to 3.

    Returns:
        bool: True if the connection succeeds, False otherwise.
    """
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
        return True
    except (socket.timeout, socket.error):
        return False

def network_required(func:callable) -> callable:
    """Decorator that ensures a network connection before executing a function.

    If no network connection is available, the decorated function will wait
    and retry until a connection is restored.

    Args:
        func (Callable): Function to decorate.

    Returns:
        Callable: Wrapped function that checks network connectivity before execution.
    """
    def wrapper(*args:tuple, **kwargs:dict[str, dict]) -> callable:
        while not is_connected():
            print("No network connection. Waiting for the reinstatement of the connection ...")
            time.sleep(5)
        return func(*args, **kwargs)
    return wrapper
