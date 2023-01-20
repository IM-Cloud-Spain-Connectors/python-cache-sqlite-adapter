from typing import List

import pytest

from rndi.cache.adapters.sqlite.adapter import SQLiteCacheAdapter
from rndi.cache.contracts import Cache


@pytest.fixture
def adapters():
    def __adapters() -> List[Cache]:
        return [
            SQLiteCacheAdapter('/tmp', 900),
        ]

    return __adapters
