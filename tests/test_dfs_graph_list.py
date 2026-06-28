from harness import load

from tests._fixtures import SAMPLE_LIST, is_valid_list_path

m = load("dfs_graph_list")


def test_finds_a_valid_path():
    path = m.dfs(SAMPLE_LIST, 0, 6)
    assert path is not None
    assert is_valid_list_path(SAMPLE_LIST, path, 0, 6)


def test_source_equals_needle():
    assert m.dfs(SAMPLE_LIST, 3, 3) == [3]


def test_unreachable_returns_none():
    # Node 0 has no outgoing edges; nothing is reachable from it.
    graph = [[], [(0, 1)]]
    assert m.dfs(graph, 0, 1) is None
