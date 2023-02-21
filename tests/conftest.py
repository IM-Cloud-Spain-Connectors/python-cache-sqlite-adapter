from __future__ import annotations

from abc import ABCMeta, abstractmethod
from logging import LoggerAdapter
from typing import Dict, List, Optional, Union
from unittest.mock import patch

import pytest
from rndi.cache.adapters.sqlite.adapter import SQLiteCacheAdapter
from rndi.cache.contracts import Cache
from rndi.cache.provider import provide_cache


@pytest.fixture
def counter():
    class Counter:
        instance: Optional[Counter] = None

        def __init__(self):
            self.count = 0

        @classmethod
        def make(cls, reset: bool = False) -> Counter:
            if not isinstance(cls.instance, Counter) or reset:
                cls.instance = Counter()
            return cls.instance

        def increase(self, step: int = 1) -> Counter:
            self.count = self.count + step
            return self

    def __(reset: bool = False) -> Counter:
        return Counter.make(reset)

    return __


@pytest.fixture
def adapters(logger):
    def __adapters() -> List[Union[Cache, HasEntry]]:
        setups = [
            {'CACHE_DRIVER': 'sqlite'},
        ]

        extra = {
            'sqlite': provide_test_sqlite_cache_adapter,
        }

        return [provide_cache(setup, logger(), extra) for setup in setups]

    return __adapters


@pytest.fixture()
def logger():
    def __logger() -> LoggerAdapter:
        with patch('logging.LoggerAdapter') as logger:
            return logger

    return __logger


class HasEntry(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def get_entry(self, key: str) -> Optional[Dict[str, Union[str, int]]]:
        """
        Get an entry from the cache, not only the value.
        This is useful for testing purposes when we want to validate the TTL.
        :param key: str The key to search for.
        :return: Optional[Dict[str, Union[str, int]]] The entry if found, None otherwise.
        """


class SQLiteCacheAdapterTester(SQLiteCacheAdapter, HasEntry):
    def get_entry(self, key: str) -> Optional[Dict[str, Union[str, int]]]:
        with self.connection as connection:
            entry = next(connection.execute(self._get_sql, (key,)))

        if entry is None:
            return None

        return {
            'value': entry[0],
            'expire_at': entry[1],
        }


def provide_test_sqlite_cache_adapter(config: dict) -> Cache:
    return SQLiteCacheAdapterTester(
        directory_path=config.get('CACHE_DIR', '/tmp/cache'),
        ttl=config.get('CACHE_TTL', 900),
        name=config.get('CACHE_SQLITE_NAME', 'cache'),
        options={
            'check_same_thread': config.get('CACHE_SQLITE_CHECK_SAME_THREAD', 'False') == 'True',
            'timeout': float(config.get('CACHE_SQLITE_TIMEOUT', 15.0)),
        },
    )
