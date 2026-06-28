import random

from harness import load

m = load("insertion_sort")


def test_sorts_in_place():
    arr = [5, 2, 9, 1, 5, 6]
    result = m.insertion_sort(arr)
    assert result is None, "insertion_sort should sort in place and return None"
    assert arr == [1, 2, 5, 5, 6, 9]


def test_edge_cases():
    for arr, expected in [([], []), ([1], [1]), ([2, 1], [1, 2])]:
        m.insertion_sort(arr)
        assert arr == expected


def test_random_matches_builtin():
    rng = random.Random(1)
    for _ in range(50):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(0, 30))]
        expected = sorted(arr)
        m.insertion_sort(arr)
        assert arr == expected
