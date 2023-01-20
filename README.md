# Python Cache SQLite Adapter

[![Test](https://github.com/othercodes/python-cache-sqlite-adapter/actions/workflows/test.yml/badge.svg)](https://github.com/othercodes/python-cache-sqlite-adapter/actions/workflows/test.yml)

Provides a SQLite implementation of the Cache Interface for Python.

## Installation

The easiest way to install the Cache SQLite Adapter is to get the latest version from PyPI:

```bash
# using poetry
poetry add rndi-cache-sqlite-adapter
# using pip
pip install rndi-cache-sqlite-adapter
```

## The Contract

The used interface is `rndi.cache_interface.contracts.Cache`.

## The Adapter

Just initialize the class you want and use the public methods:

```python
from rndi.cache.contracts import Cache
from rndi.cache.adapters.sqlite.adapter import SQLiteCacheAdapter


def some_process_that_requires_cache(cache: Cache):
    # retrieve the data from cache, ir the key is not cached yet and the default 
    # value is a callable the cache will use it to compute and cache the value
    user = cache.get('user-id', lambda: db_get_user('user-id'))

    print(user)


# inject the desired cache adapter.
cache = SQLiteCacheAdapter('/tmp', 900)
some_process_that_requires_cache(cache)
```

