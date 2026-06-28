from harness import load

m = load("map")


def make():
    return m.HashMap()


def test_set_get():
    h = make()
    h.set("a", 1)
    h.set("b", 2)
    assert h.get("a") == 1
    assert h.get("b") == 2
    assert h.length == 2


def test_update_existing_key():
    h = make()
    h.set("a", 1)
    h.set("a", 99)
    assert h.get("a") == 99
    assert h.length == 1


def test_missing_key_returns_none():
    h = make()
    assert h.get("nope") is None


def test_remove():
    h = make()
    h.set("a", 1)
    assert h.remove("a") == 1
    assert h.get("a") is None
    assert h.length == 0
    assert h.remove("a") is None


def test_resize_keeps_all_entries():
    h = make()
    for i in range(100):  # forces multiple resizes
        h.set(i, i * i)
    assert h.length == 100
    for i in range(100):
        assert h.get(i) == i * i


def test_integer_and_string_keys():
    h = make()
    h.set(1, "one")
    h.set("1", "string-one")
    assert h.get(1) == "one"
    assert h.get("1") == "string-one"
