from harness import load

m = load("linear_search")


def test_found():
    assert m.linear_search([1, 3, 5, 7, 9], 5) == 2


def test_first_and_last():
    assert m.linear_search([4, 2, 8], 4) == 0
    assert m.linear_search([4, 2, 8], 8) == 2


def test_not_found():
    assert m.linear_search([1, 2, 3], 99) == -1


def test_empty():
    assert m.linear_search([], 1) == -1


def test_unsorted_ok():
    assert m.linear_search([9, 1, 7, 3], 7) == 2
