# helpers/caches.py
# warning this file is depenent on django cache

import hashlib
import pickle
from functools import wraps

import redis
from django.core.cache import cache

from helpers.loggers import logger

CACHE_TIMEOUT_15_MINUTES = 60 * 15
CACHE_TIMEOUT_30_MINUTES = 60 * 30
CACHE_TIMEOUT_1_HOUR = 60 * 60
CACHE_TIMEOUT_2_HOURS = 60 * 60 * 2
CACHE_TIMEOUT_3_HOURS = 60 * 60 * 3
CACHE_TIMEOUT_4_HOURS = 60 * 60 * 4
CACHE_TIMEOUT_24_HOURS = 60 * 60 * 24
CACHE_TIMEOUT_7_DAYS = 60 * 60 * 24 * 7
CACHE_TIMEOUT_30_DAYS = 60 * 60 * 24 * 30


def get_key_from_cache(key):
    # general logic for the key is url + params
    # add count logic
    return cache.get(key)


def set_key_to_cache(key, value, timeout=None):
    logger.debug(f"Setting {key} to cache with {timeout=}.")
    return cache.set(key, value, timeout)


def add_key_to_cache(key, value, timeout=None) -> bool:
    return cache.add(key, value, timeout)


def delete_key_from_cache(key):
    return cache.delete(key)


def generate_redis_key_from_args(*args) -> str:
    """Generate a Redis key from kwargs using pickle."""
    # Convert kwargs to a byte stream using pickle
    serialized_kwargs = pickle.dumps(args)

    # Generate an MD5 hash of the byte stream
    return hashlib.md5(serialized_kwargs).hexdigest()


def generate_redis_key_from_kwargs(**kwargs) -> str:
    """Generate a Redis key from kwargs using pickle."""
    # Convert kwargs to a byte stream using pickle
    serialized_kwargs = pickle.dumps(kwargs)

    # Generate an MD5 hash of the byte stream
    return hashlib.md5(serialized_kwargs).hexdigest()


def redis_memoize_sync(cache_timeout=60):  # 1 minute
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            args_keys = generate_redis_key_from_args(*args)
            kwargs_key = generate_redis_key_from_kwargs(**kwargs)
            cache_key = f"/{func.__name__}/{args_keys}/{kwargs_key}/"

            cache_result = get_key_from_cache(cache_key)
            if cache_result is not None:
                logger.success(f"[redis_memoize_sync] {cache_key} found in cache.")
                return cache_result

            result = func(*args, **kwargs)
            set_key_to_cache(cache_key, result, cache_timeout)

            return result

        return wrapper

    return decorator


def get_ttl(key):
    ttl = cache.ttl(key)
    if ttl is None:
        if cache.get(key) is None:
            return "Key does not exist in cache."
        else:
            return "Key exists but does not have an expiry."
    else:
        return f"TTL for {key} is {ttl} seconds."


def get_all_redis_keys():
    # Get the raw Redis client from the cache
    redis_client = cache.client.get_client()

    # Use the Redis client to get all keys
    keys = redis_client.keys("*")

    # Return the keys
    return keys


def delete_keyword_from_cache(keyword):
    keys = get_all_redis_keys()
    for key in keys:
        cache_key = key.decode("utf-8").split(":")[-1]
        if keyword in cache_key:
            print(f"Deleting {cache_key}")
            cache.delete(cache_key)


def get_redis_space():
    # Connect to your Redis server
    r = redis.Redis(host="redis-oraclus", port=6379, db=0)

    # Get memory info
    info = r.info("memory")

    memory_limit = info["maxmemory"]
    memory_limit_mb = memory_limit / (1024 * 1024)
    print(f"Memory Limit: {memory_limit_mb:.2f} MB")

    memory_used = info["used_memory"]
    memory_used_mb = memory_used / (1024 * 1024)
    print(f"Used Memory: {memory_used_mb:.2f} MB")

    memory_left = memory_limit - memory_used
    memory_left_mb = memory_left / (1024 * 1024)
    print(f"Memory left: {memory_left_mb:.2f} MB")

    keys = r.keys("*")
    print(f"Number of keys: {len(keys)}")

    avg_key_size = sum(r.memory_usage(key) for key in keys) / len(keys)
    print(f"Avg key size: {avg_key_size:.2f} bytes")

    number_of_more_keys = memory_left // avg_key_size
    print(f"Number of more keys: {number_of_more_keys}")
