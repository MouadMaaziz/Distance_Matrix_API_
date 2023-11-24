
from functools import wraps
import os
import json





def cached(func):
    """Decorator function to cache API responses."""

    # Set up caching
    CACHE_FILE = 'cache.json'
    if os.path.isfile(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
    else:
        cache = {}


    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cache:
            return cache[key]
        else:
            result = func(*args, **kwargs)
            cache[key] = result
            with open(CACHE_FILE, 'w') as f:
                json.dump(cache, f)
            return result
    return wrapper