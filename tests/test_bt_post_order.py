from harness import load

from tests._fixtures import SAMPLE_TREE_LEVEL_ORDER, build_tree

m = load("bt_post_order")


def test_sample_tree():
    root = build_tree(SAMPLE_TREE_LEVEL_ORDER)
    assert m.post_order(root) == [5, 15, 10, 30, 100, 50, 20]


def test_empty():
    assert m.post_order(None) == []


def test_single_node():
    assert m.post_order(build_tree([42])) == [42]
