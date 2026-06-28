from harness import load

m = load("lru")


def test_basic_get_update():
    cache = m.LRU(2)
    cache.update("a", 1)
    cache.update("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_missing_key_returns_none():
    cache = m.LRU(2)
    assert cache.get("x") is None


def test_evicts_least_recently_used():
    cache = m.LRU(2)
    cache.update("a", 1)
    cache.update("b", 2)
    cache.update("c", 3)  # capacity exceeded -> evict "a"
    assert cache.get("a") is None
    assert cache.get("b") == 2
    assert cache.get("c") == 3


def test_get_refreshes_recency():
    cache = m.LRU(2)
    cache.update("a", 1)
    cache.update("b", 2)
    assert cache.get("a") == 1  # "a" is now most-recently used
    cache.update("c", 3)  # evicts "b", not "a"
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


def test_update_existing_refreshes_and_overwrites():
    cache = m.LRU(2)
    cache.update("a", 1)
    cache.update("b", 2)
    cache.update("a", 10)  # refresh + overwrite "a"
    cache.update("c", 3)  # evicts "b"
    assert cache.get("a") == 10
    assert cache.get("b") is None
    assert cache.get("c") == 3
