# helpers/decorators.py
import asyncio
import hashlib
import time
from functools import wraps

from django.core.cache import cache

from helpers.loggers import logger


def timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time
        logger.debug(f"[TIMER] {func.__name__} took {elapsed_time:.2f} seconds")
        return result

    return wrapper


def timer_decorator_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed_time = time.perf_counter() - start_time
        logger.debug(f"[TIMER] {func.__name__} took {elapsed_time:.2f} seconds")
        return result

    return wrapper


# TODO replace with from asyncstdlib import cached_property
def cache_result_async(timeout=60 * 60, cache_key=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if cache_key is None:
                raw_key = f"{func.__name__}-{args}-{kwargs}"
                # Hash the key to ensure it has a fixed size
                key = hashlib.sha256(raw_key.encode()).hexdigest()
            else:
                key = cache_key

            # Try to fetch the result from cache
            result = cache.get(key)
            if result is not None:
                # Result found in cache
                return result
            else:
                # Result not found in cache, calculate it
                logger.debug(f"Warming up cache: {func.__name__}")
                # Check if the function is async, and await it if necessary
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                # Store the result in cache for next time
                cache.set(key, result, timeout)
                return result

        return wrapper

    return decorator


# todo move to common/cache.py
def update_cache_function(func_name, args, kwargs, new_value, timeout=60 * 60):
    raw_key = f"{func_name}-{args}-{kwargs}"
    # Hash the key to ensure it has a fixed size
    key = hashlib.sha256(raw_key.encode()).hexdigest()
    # Store the new value in the cache
    cache.set(key, new_value, timeout)
