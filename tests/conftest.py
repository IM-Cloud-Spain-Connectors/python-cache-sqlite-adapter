from typing import List

import pytest

from rndi.cache_interface.contracts import Cache
from rndi.cache_sqlite_adapter.adapters import SQLiteCacheAdapter


@pytest.fixture
def adapters():
    def __adapters() -> List[Cache]:
        return [
            SQLiteCacheAdapter('/tmp', 900),
        ]

    return __adapters
