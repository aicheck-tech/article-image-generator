"""Cache instances to be reused easily."""
from functools import lru_cache

_CACHED_SERVICES = []


def service(func):
    """
    Decorator to cache the services, so they don't need to be created again and again.
    All services are also tracked, so it is possible to invalidate the cache for the all of them.
    """
    cached_service = lru_cache(maxsize=1)(func)
    _CACHED_SERVICES.append(cached_service)
    return cached_service
