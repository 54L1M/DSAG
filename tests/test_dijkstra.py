from harness import load

from tests._fixtures import SAMPLE_LIST

m = load("dijkstra")


def _path_weight(graph, path):
    total = 0
    for a, b in zip(path, path[1:], strict=False):
        total += next(w for to, w in graph[a] if to == b)
    return total


def test_shortest_path():
    path = m.dijkstra(SAMPLE_LIST, 0, 6)
    assert path == [0, 1, 4, 5, 6]
    assert _path_weight(SAMPLE_LIST, path) == 7


def test_source_equals_sink():
    assert m.dijkstra(SAMPLE_LIST, 4, 4) == [4]


def test_unreachable_returns_empty():
    graph = [[(1, 1)], [(0, 1)], []]  # node 2 is isolated
    assert m.dijkstra(graph, 0, 2) == []


def test_prefers_cheaper_longer_route():
    # 0->1 direct costs 10, but 0->2->1 costs 1+1=2.
    graph = [
        [(1, 10), (2, 1)],
        [(0, 10), (2, 1)],
        [(0, 1), (1, 1)],
    ]
    assert m.dijkstra(graph, 0, 1) == [0, 2, 1]
