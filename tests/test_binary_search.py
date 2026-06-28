from harness import load

m = load("binary_search")


def test_found_various():
    arr = [1, 3, 5, 7, 9, 11]
    for i, v in enumerate(arr):
        assert m.binary_search(arr, v) == i


def test_not_found():
    assert m.binary_search([1, 3, 5, 7, 9], 6) == -1
    assert m.binary_search([1, 3, 5, 7, 9], 0) == -1
    assert m.binary_search([1, 3, 5, 7, 9], 100) == -1


def test_empty():
    assert m.binary_search([], 1) == -1


def test_single():
    assert m.binary_search([42], 42) == 0
    assert m.binary_search([42], 7) == -1
