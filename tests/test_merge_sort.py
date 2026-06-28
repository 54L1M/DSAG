import random

from harness import load

m = load("merge_sort")


def test_returns_new_sorted_list():
    arr = [5, 2, 9, 1, 5, 6]
    result = m.merge_sort(arr)
    assert result == [1, 2, 5, 5, 6, 9]


def test_edge_cases():
    assert m.merge_sort([]) == []
    assert m.merge_sort([1]) == [1]
    assert m.merge_sort([2, 1]) == [1, 2]


def test_random_matches_builtin():
    rng = random.Random(2)
    for _ in range(50):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        assert m.merge_sort(arr) == sorted(arr)
