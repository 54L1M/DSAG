from harness import load

from tests._fixtures import SAMPLE_TREE_LEVEL_ORDER, build_tree

m = load("bt_in_order")


def test_sample_tree_is_sorted():
    root = build_tree(SAMPLE_TREE_LEVEL_ORDER)
    assert m.in_order(root) == [5, 10, 15, 20, 30, 50, 100]


def test_empty():
    assert m.in_order(None) == []


def test_single_node():
    assert m.in_order(build_tree([42])) == [42]
