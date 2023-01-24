import pytest
from logging import LoggerAdapter
from typing import List
from unittest.mock import patch

from rndi.cache.adapters.sqlite.adapter import provide_sqlite_cache_adapter
from rndi.cache.contracts import Cache
from rndi.cache.provider import provide_cache


@pytest.fixture
def adapters(logger):
    def __adapters() -> List[Cache]:
        setups = [
            {'CACHE_DRIVER': 'sqlite'},
        ]

        extra = {
            'sqlite': provide_sqlite_cache_adapter
        }

        return [provide_cache(setup, logger(), extra) for setup in setups]

    return __adapters


@pytest.fixture()
def logger():
    def __logger() -> LoggerAdapter:
        with patch('logging.LoggerAdapter') as logger:
            return logger

    return __logger
