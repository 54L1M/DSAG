import random

from harness import load

m = load("min_heap")


def test_pops_in_sorted_order():
    h = m.MinHeap()
    for v in (5, 3, 8, 1, 9, 2):
        h.insert(v)
    assert h.length == 6
    out = [h.delete() for _ in range(6)]
    assert out == [1, 2, 3, 5, 8, 9]
    assert h.length == 0


def test_empty_delete_returns_none():
    h = m.MinHeap()
    assert h.delete() is None


def test_interleaved_insert_delete():
    h = m.MinHeap()
    h.insert(5)
    h.insert(3)
    assert h.delete() == 3
    h.insert(1)
    h.insert(4)
    assert h.delete() == 1
    assert h.delete() == 4
    assert h.delete() == 5
    assert h.delete() is None


def test_random_matches_sorted():
    rng = random.Random(7)
    for _ in range(30):
        values = [rng.randint(-100, 100) for _ in range(rng.randint(0, 50))]
        h = m.MinHeap()
        for v in values:
            h.insert(v)
        out = [h.delete() for _ in range(len(values))]
        assert out == sorted(values)
