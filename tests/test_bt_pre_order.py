from harness import load

from tests._fixtures import SAMPLE_TREE_LEVEL_ORDER, build_tree

m = load("bt_pre_order")


def test_sample_tree():
    root = build_tree(SAMPLE_TREE_LEVEL_ORDER)
    assert m.pre_order(root) == [20, 10, 5, 15, 50, 30, 100]


def test_empty():
    assert m.pre_order(None) == []


def test_single_node():
    assert m.pre_order(build_tree([42])) == [42]
