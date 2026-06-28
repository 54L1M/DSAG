from harness import load

m = load("trie")


def make():
    return m.Trie()


def test_insert_and_contains():
    t = make()
    t.insert("cat")
    assert t.contains("cat") is True
    assert t.contains("ca") is False  # prefix is not a full word
    assert t.contains("cats") is False


def test_starts_with_autocomplete():
    t = make()
    for w in ("cat", "car", "card", "dog"):
        t.insert(w)
    assert t.starts_with("ca") == ["car", "card", "cat"]
    assert t.starts_with("car") == ["car", "card"]
    assert t.starts_with("do") == ["dog"]
    assert t.starts_with("z") == []


def test_delete():
    t = make()
    t.insert("cat")
    t.insert("car")
    t.delete("cat")
    assert t.contains("cat") is False
    assert t.contains("car") is True
    # deleting a missing word is a no-op
    t.delete("nope")
    assert t.starts_with("ca") == ["car"]


def test_prefix_is_word_too():
    t = make()
    t.insert("car")
    t.insert("card")
    assert t.contains("car") is True
    assert t.starts_with("car") == ["car", "card"]
