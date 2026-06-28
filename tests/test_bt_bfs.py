from harness import load

from tests._fixtures import SAMPLE_TREE_LEVEL_ORDER, build_tree

m = load("bt_bfs")


def test_sample_tree_level_order():
    root = build_tree(SAMPLE_TREE_LEVEL_ORDER)
    assert m.bfs(root) == [20, 10, 50, 5, 15, 30, 100]


def test_empty():
    assert m.bfs(None) == []


def test_unbalanced():
    # 1 -> right 2 -> right 3 (a right-leaning chain)
    root = build_tree([1, None, 2, None, 3])
    assert m.bfs(root) == [1, 2, 3]
