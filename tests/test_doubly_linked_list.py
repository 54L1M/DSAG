import pytest
from harness import load

m = load("doubly_linked_list")


def make():
    return m.DoublyLinkedList()


def test_append_prepend_get():
    ll = make()
    ll.append(2)
    ll.append(3)
    ll.prepend(1)
    assert ll.length == 3
    assert [ll.get(i) for i in range(3)] == [1, 2, 3]


def test_insert_at():
    ll = make()
    ll.append(1)
    ll.append(3)
    ll.insert_at(2, 1)
    ll.insert_at(0, 0)
    ll.insert_at(4, 4)
    assert [ll.get(i) for i in range(5)] == [0, 1, 2, 3, 4]


def test_remove_at_all_positions():
    ll = make()
    for v in (1, 2, 3, 4):
        ll.append(v)
    assert ll.remove_at(0) == 1  # head
    assert ll.remove_at(2) == 4  # tail
    assert ll.remove_at(0) == 2
    assert ll.remove_at(0) == 3
    assert ll.length == 0


def test_remove_value_and_relink():
    ll = make()
    for v in (1, 2, 3):
        ll.append(v)
    assert ll.remove(2) == 2
    assert [ll.get(0), ll.get(1)] == [1, 3]
    # list still walkable after a middle removal
    ll.append(4)
    assert [ll.get(i) for i in range(3)] == [1, 3, 4]
    assert ll.remove(99) is None


def test_out_of_range_raises():
    ll = make()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(5)
    with pytest.raises(IndexError):
        ll.remove_at(5)
    with pytest.raises(IndexError):
        ll.insert_at(9, 5)
