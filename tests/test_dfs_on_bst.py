from harness import load

from tests._fixtures import build_bst

m = load("dfs_on_bst")


def test_finds_present_values():
    root = build_bst([20, 10, 50, 5, 15, 30, 100])
    for v in (20, 10, 50, 5, 15, 30, 100):
        assert m.find(root, v) is True


def test_missing_values():
    root = build_bst([20, 10, 50, 5, 15, 30, 100])
    for v in (0, 11, 99, 1000):
        assert m.find(root, v) is False


def test_empty_tree():
    assert m.find(None, 5) is False
