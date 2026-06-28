from harness import load

from tests._fixtures import build_tree

m = load("compare_binary_trees")


def test_equal_trees():
    a = build_tree([1, 2, 3, 4, 5])
    b = build_tree([1, 2, 3, 4, 5])
    assert m.compare(a, b) is True


def test_both_empty():
    assert m.compare(None, None) is True


def test_different_values():
    a = build_tree([1, 2, 3])
    b = build_tree([1, 2, 4])
    assert m.compare(a, b) is False


def test_different_structure():
    a = build_tree([1, 2, 3, 4])
    b = build_tree([1, 2, 3])
    assert m.compare(a, b) is False


def test_one_empty():
    assert m.compare(build_tree([1]), None) is False
    assert m.compare(None, build_tree([1])) is False
