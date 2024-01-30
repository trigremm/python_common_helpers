# helpers/classes.py


from abc import ABC, abstractmethod

from helpers.caches import add_key_to_cache, delete_key_from_cache, get_key_from_cache, set_key_to_cache
from helpers.exceptions import DeduplicateLockException


class SynchronousCacheableServiceABC(ABC):
    @classmethod
    def generate_cache_key(cls):
        raise NotImplementedError

    @property
    @abstractmethod
    def cache_key(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def cache_timeout(self):
        raise NotImplementedError

    @abstractmethod
    def main(self):
        raise NotImplementedError

    def invalidate_cache_result(self):
        cache_key = self.cache_key
        set_key_to_cache(cache_key, None, timeout=0)

    def set_result_to_cache(self):
        cache_key = self.cache_key
        cache_timeout = self.cache_timeout
        result = self.main()
        set_key_to_cache(cache_key, result, timeout=cache_timeout)
        return result

    def get_result_from_cache(self):
        cache_key = self.cache_key
        result = get_key_from_cache(cache_key)
        if result is None:
            result = self.set_result_to_cache()
        return result


class CachableServiceABC(ABC):
    @property
    @abstractmethod
    def cache_key(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def cache_timeout(self):
        raise NotImplementedError

    @abstractmethod
    async def main(self):
        raise NotImplementedError

    async def set_result_to_cache(self):
        cache_key = self.cache_key
        cache_timeout = self.cache_timeout
        result = await self.main()
        set_key_to_cache(cache_key, result, timeout=cache_timeout)
        return result

    async def get_result_from_cache(self):
        cache_key = self.cache_key
        result = get_key_from_cache(cache_key)
        if result is None:
            result = await self.set_result_to_cache()
        return result


class LockableHeavyCalculationsServiceABC(ABC):
    @property
    @abstractmethod
    def dedup_lock_key(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def dedup_lock_timeout(self):
        raise NotImplementedError

    @abstractmethod
    async def heavy_calculations(self):
        raise NotImplementedError

    async def heavy_calculations_with_lock(self):
        lock_key = self.dedup_lock_key
        lock_timeout = self.dedup_lock_timeout

        if add_key_to_cache(lock_key, "true", timeout=lock_timeout):
            try:
                result = await self.heavy_calculations()
            finally:
                # Ensure lock is released
                delete_key_from_cache(lock_key)
            return result
        else:
            raise DeduplicateLockException(f"[MAIN_IS_LOCKED] {lock_key=}")


class CachableLockableServiceABC(CachableServiceABC, LockableHeavyCalculationsServiceABC):
    pass


class ExampleUsageClass(CachableLockableServiceABC):
    @property
    def cache_key(self):
        return "cache_key"

    @property
    def cache_timeout(self):
        return 60 * 60

    @property
    def dedup_lock_key(self):
        return f"/dedup/lock/key/{self.cache_key}"

    @property
    def dedup_lock_timeout(self):
        return 60 * 10

    async def main(self):
        # Ensure the caching is done with a lock
        return await self.heavy_calculations_with_lock()

    async def heavy_calculations(self):
        # You can put your actual heavy calculation logic here
        return 1
