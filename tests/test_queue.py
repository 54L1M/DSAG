from harness import load

m = load("queue")


def test_fifo_order():
    q = m.Queue()
    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    assert q.length == 3
    assert q.peek() == 1
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.length == 1
    assert q.peek() == 3


def test_empty_returns_none():
    q = m.Queue()
    assert q.dequeue() is None
    assert q.peek() is None
    assert q.length == 0


def test_enqueue_after_emptying():
    q = m.Queue()
    q.enqueue(1)
    assert q.dequeue() == 1
    q.enqueue(2)
    assert q.peek() == 2
    assert q.dequeue() == 2
    assert q.dequeue() is None
