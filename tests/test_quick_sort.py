import random

from harness import load

m = load("quick_sort")


def test_sorts_in_place():
    arr = [5, 2, 9, 1, 5, 6]
    result = m.quick_sort(arr)
    assert result is None, "quick_sort should sort in place and return None"
    assert arr == [1, 2, 5, 5, 6, 9]


def test_edge_cases():
    for arr, expected in [([], []), ([1], [1]), ([3, 2, 1], [1, 2, 3])]:
        m.quick_sort(arr)
        assert arr == expected


def test_duplicates():
    arr = [4, 4, 4, 4]
    m.quick_sort(arr)
    assert arr == [4, 4, 4, 4]


def test_random_matches_builtin():
    rng = random.Random(3)
    for _ in range(50):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        expected = sorted(arr)
        m.quick_sort(arr)
        assert arr == expected
