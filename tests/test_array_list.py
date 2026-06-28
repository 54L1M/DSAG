import pytest
from harness import load

m = load("array_list")


def test_push_get():
    al = m.ArrayList()
    for v in range(10):  # forces several capacity doublings
        al.push(v)
    assert al.length == 10
    assert [al.get(i) for i in range(10)] == list(range(10))


def test_set():
    al = m.ArrayList()
    al.push(1)
    al.push(2)
    al.set(1, 99)
    assert al.get(1) == 99


def test_pop():
    al = m.ArrayList()
    for v in (1, 2, 3):
        al.push(v)
    assert al.pop() == 3
    assert al.length == 2
    assert al.pop() == 2
    assert al.pop() == 1
    assert al.pop() is None


def test_insert_at_and_remove_at():
    al = m.ArrayList()
    for v in (1, 2, 4):
        al.push(v)
    al.insert_at(3, 2)  # -> 1, 2, 3, 4
    al.insert_at(0, 0)  # front
    al.insert_at(5, al.length)  # end
    assert [al.get(i) for i in range(al.length)] == [0, 1, 2, 3, 4, 5]
    assert al.remove_at(0) == 0
    assert al.remove_at(al.length - 1) == 5
    assert [al.get(i) for i in range(al.length)] == [1, 2, 3, 4]


def test_out_of_range_raises():
    al = m.ArrayList()
    al.push(1)
    with pytest.raises(IndexError):
        al.get(5)
    with pytest.raises(IndexError):
        al.set(5, 9)
    with pytest.raises(IndexError):
        al.remove_at(5)
    with pytest.raises(IndexError):
        al.insert_at(9, 5)


def test_falsy_values_roundtrip():
    al = m.ArrayList()
    al.push(0)
    al.push(0)
    assert al.length == 2
    assert al.get(0) == 0
    assert al.pop() == 0
