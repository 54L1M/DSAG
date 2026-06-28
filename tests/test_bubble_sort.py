import random

from harness import load

m = load("bubble_sort")


def test_sorts_in_place():
    arr = [5, 2, 9, 1, 5, 6]
    result = m.bubble_sort(arr)
    assert result is None, "bubble_sort should sort in place and return None"
    assert arr == [1, 2, 5, 5, 6, 9]


def test_already_sorted():
    arr = [1, 2, 3, 4]
    m.bubble_sort(arr)
    assert arr == [1, 2, 3, 4]


def test_reversed():
    arr = [5, 4, 3, 2, 1]
    m.bubble_sort(arr)
    assert arr == [1, 2, 3, 4, 5]


def test_empty_and_single():
    a: list[int] = []
    m.bubble_sort(a)
    assert a == []
    b = [7]
    m.bubble_sort(b)
    assert b == [7]


def test_random_matches_builtin():
    rng = random.Random(0)
    for _ in range(50):
        arr = [rng.randint(-50, 50) for _ in range(rng.randint(0, 30))]
        expected = sorted(arr)
        m.bubble_sort(arr)
        assert arr == expected
