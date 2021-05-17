import time
from enum import Enum
from json import dumps

from redis import Redis
import cacheout
from datetime import datetime, timezone


class CacheConfiguration(Enum):
    DISABLED = 0
    MEMORY = 1
    REDIS = 2


class Cache:
    def __init__(self, configuration_type: CacheConfiguration, **configuration):
        self._configuration_type = configuration_type
        self._configuration = configuration_type
        self._disabled = False
        if configuration_type == CacheConfiguration.DISABLED:
            self._disabled = True
        elif configuration_type == CacheConfiguration.MEMORY:
            self._cache = cacheout.Cache(
                maxsize=64, ttl=3 * 60, timer=time.time, default=None
            )
        elif configuration_type == CacheConfiguration.REDIS:
            self._redis = Redis(**configuration)

    def key_exists(self, key):
        if self._configuration_type == CacheConfiguration.MEMORY:
            return self._cache.has(key)
        elif self._configuration_type == CacheConfiguration.REDIS:
            return self._redis.exists(key)

    def get_value(self, key):
        if self._configuration_type == CacheConfiguration.MEMORY:
            return self._cache.get(key, None)
        elif self._configuration_type == CacheConfiguration.REDIS:
            return self._redis.get(key)

    def set_value(self, key, value, expiry=None):
        if self._configuration_type == CacheConfiguration.MEMORY:
            self._cache.set(key, value, ttl=expiry)
        elif self._configuration_type == CacheConfiguration.REDIS:
            self._redis.set(key, value, ex=expiry)

    def add_cache(self, full_url, value, cache_date, cache_time):
        if not self._disabled:
            if type(value) == dict:
                value = dumps(value)
            expiry = cache_time - (datetime.now(timezone.utc) - cache_date).total_seconds()
            if expiry > 0:
                self.set_value(full_url, value, expiry=expiry)

    def read_cache(self, full_url):
        if not self._disabled:
            value = self.get_value(full_url)
            if value:
                return value
