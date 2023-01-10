COUNT = 0
COMPLEX_KEY = 'https://some.url.com/id/8b3a6052-621e-45cc-be5a-316f486c50aa'


def increment(reset: bool = False):
    global COUNT
    if reset:
        COUNT = 0
    COUNT = COUNT + 1
    return COUNT


def test_adapter_cache_should_return_false_if_has_not_cached_key(adapters):
    for adapter in adapters():
        assert not adapter.has('missing-key')


def test_adapter_cache_should_cache_values_by_key(adapters):
    for adapter in adapters():
        a = adapter.get(COMPLEX_KEY, lambda: (increment(True), 20))
        b = adapter.get(COMPLEX_KEY)

        assert 1 == a == b
        assert adapter.has(COMPLEX_KEY)


def test_adapter_cache_should_delete_expired_values(adapters):
    for adapter in adapters():
        adapter.put('x', 'some-value-1', 3600)
        adapter.put('y', 'some-value-2', 0)
        adapter.put('z', 'some-value-3', 0)

        assert adapter.has('x')
        assert not adapter.has('y')
        assert not adapter.has('z')


def test_adapter_cache_should_delete_value_by_key(adapters):
    for adapter in adapters():
        adapter.put('b', 'some-value')
        adapter.delete('b')
        adapter.delete('missing-key')

        assert not adapter.has('b')
        assert not adapter.has('missing-key')


def test_adapter_cache_should_flush_all_values(adapters):
    for adapter in adapters():
        adapter.put('b', 'some-value-1')
        adapter.put('c', 'some-value-2')
        adapter.put('d', 'some-value-3')

        adapter.flush()

        assert not adapter.has('b')
        assert not adapter.has('c')
        assert not adapter.has('d')


def test_adapter_cache_should_flush_only_expired_values(adapters):
    for adapter in adapters():
        adapter.put('x', 'some-value-1', 3600)
        adapter.put('y', 'some-value-2', 0)
        adapter.put('z', 'some-value-3', 0)

        adapter.flush(expired_only=True)

        assert adapter.has('x')
        assert not adapter.has('y')
        assert not adapter.has('z')
