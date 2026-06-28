from harness import load

from tests._fixtures import (
    SAMPLE_UNDIRECTED,
    SAMPLE_UNDIRECTED_MST_WEIGHT,
    collect_mst_edges,
    is_connected_spanning_tree,
)

m = load("prim")


def test_returns_spanning_tree():
    mst = m.prims(SAMPLE_UNDIRECTED)
    assert mst is not None
    assert is_connected_spanning_tree(mst, len(SAMPLE_UNDIRECTED))


def test_total_weight_is_minimal():
    mst = m.prims(SAMPLE_UNDIRECTED)
    total = sum(w for _a, _b, w in collect_mst_edges(mst))
    assert total == SAMPLE_UNDIRECTED_MST_WEIGHT


def test_empty_graph_returns_none():
    assert m.prims([]) is None
