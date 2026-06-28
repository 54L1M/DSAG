from harness import load

m = load("stack")


def test_lifo_order():
    s = m.Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.length == 3
    assert s.peek() == 3
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.length == 1
    assert s.peek() == 1


def test_empty_returns_none():
    s = m.Stack()
    assert s.pop() is None
    assert s.peek() is None
    assert s.length == 0


def test_push_after_emptying():
    s = m.Stack()
    s.push(1)
    assert s.pop() == 1
    s.push(2)
    assert s.peek() == 2
    assert s.pop() == 2
    assert s.pop() is None
