"""Grumo cache capability — key/value caching (Sprint 13).

``MemoryCache`` is the default provider: process-local, no TTL, no
persistence. ``RedisCache`` (``[redis]`` extra) is the production backend
with TTL support and durability.
"""

from grumo.storage.cache.interfaces import CacheCapabilities, GrumoCache
from grumo.storage.cache.memory import MemoryCache
from grumo.storage.cache.redis import RedisCache

__all__ = ["CacheCapabilities", "MemoryCache", "RedisCache", "GrumoCache"]
