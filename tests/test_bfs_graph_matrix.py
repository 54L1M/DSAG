from harness import load

from tests._fixtures import SAMPLE_MATRIX

m = load("bfs_graph_matrix")


def test_finds_shortest_hop_path():
    assert m.bfs(SAMPLE_MATRIX, 0, 3) == [0, 1, 3]


def test_source_equals_needle():
    assert m.bfs(SAMPLE_MATRIX, 2, 2) == [2]


def test_unreachable_returns_none():
    # No edge leads into node 0, so 3 -> 0 is impossible.
    assert m.bfs(SAMPLE_MATRIX, 3, 0) is None
