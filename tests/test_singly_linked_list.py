import pytest
from harness import load

m = load("singly_linked_list")


def make():
    return m.SinglyLinkedList()


def test_append_and_get():
    ll = make()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.length == 3
    assert [ll.get(i) for i in range(3)] == [1, 2, 3]


def test_prepend():
    ll = make()
    ll.prepend(1)
    ll.prepend(2)
    assert [ll.get(0), ll.get(1)] == [2, 1]
    assert ll.length == 2


def test_insert_at():
    ll = make()
    ll.append(1)
    ll.append(3)
    ll.insert_at(2, 1)
    assert [ll.get(i) for i in range(3)] == [1, 2, 3]
    ll.insert_at(0, 0)  # front
    ll.insert_at(4, 4)  # end (index == length)
    assert [ll.get(i) for i in range(5)] == [0, 1, 2, 3, 4]


def test_remove_at():
    ll = make()
    for v in (1, 2, 3):
        ll.append(v)
    assert ll.remove_at(1) == 2
    assert ll.length == 2
    assert [ll.get(0), ll.get(1)] == [1, 3]
    assert ll.remove_at(0) == 1
    assert ll.remove_at(0) == 3
    assert ll.length == 0


def test_remove_value():
    ll = make()
    for v in (1, 2, 3):
        ll.append(v)
    assert ll.remove(2) == 2
    assert ll.length == 2
    assert ll.remove(99) is None


def test_append_after_emptying_uses_tail():
    ll = make()
    ll.append(1)
    ll.remove_at(0)
    ll.append(5)
    assert ll.length == 1
    assert ll.get(0) == 5


def test_out_of_range_raises():
    ll = make()
    ll.append(1)
    with pytest.raises(IndexError):
        ll.get(5)
    with pytest.raises(IndexError):
        ll.remove_at(5)
    with pytest.raises(IndexError):
        ll.insert_at(9, 5)
