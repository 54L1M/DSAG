from harness import load

m = load("two_crystal_balls")


def _make(n: int, first_break: int) -> list[bool]:
    return [i >= first_break for i in range(n)]


def test_basic():
    breaks = _make(100, 42)
    assert m.two_crystal_balls(breaks) == 42


def test_breaks_at_zero():
    assert m.two_crystal_balls(_make(50, 0)) == 0


def test_breaks_at_last():
    assert m.two_crystal_balls(_make(50, 49)) == 49


def test_never_breaks():
    assert m.two_crystal_balls([False] * 30) == -1


def test_empty():
    assert m.two_crystal_balls([]) == -1


def test_many_positions():
    for n in (1, 2, 5, 16, 17, 64, 81, 99):
        for first in range(n):
            assert m.two_crystal_balls(_make(n, first)) == first
