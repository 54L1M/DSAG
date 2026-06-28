# Queue (FIFO) — In Depth

> In-depth companion · linear · stub: `src/topics/linear/queue.py` · test: `tests/test_queue.py`
>
> New here? Read the [quick version](queue.md) first.

## The mental model

A queue is **first in, first out (FIFO)**: the item that has waited longest
leaves first, like a line at a shop. Two operations: `enqueue` joins the back,
`dequeue` serves the front. `peek` looks at the front without removing it.

The clever bit is the implementation. A queue is *just a singly linked list*
where we only ever touch two specific ends:

```
front (head)                      back (tail)
   |                                  |
   v                                  v
 [1|•] -> [2|•] -> [3|•] -> None
   ^dequeue here          ^enqueue here
```

- **`head` = front**: where we dequeue and peek.
- **`tail` = back**: where we enqueue.

Both ends are O(1) on a linked list (head removal and tail-pointer append), so
the whole queue is O(1). The node and fields are the familiar trio:

```python
class _Node:
    __slots__ = ("value", "next")
# Queue holds: head, tail, length
```

## Why it works — the invariant

1. **`length` equals the node count** from `head` to `None`.
2. **`head` is the oldest element, `tail` the newest.** FIFO falls out of always
   removing from `head` and always adding at `tail`.
3. **`tail.next is None`** — the back is genuinely the last node.
4. **Empty ⟺ `head is None` ⟺ `tail is None` ⟺ `length == 0`.** All three move
   together.

The direction discipline is what *makes* it FIFO. If you ever dequeued from the
tail, you'd have a stack, not a queue. The structure is identical; the choice of
which end to remove from is the entire difference between FIFO and LIFO.

## Detailed walkthrough

**`enqueue(item)` — O(1).** Hang the new node off `tail`, advance `tail`.

```
before:  head -> [1|•] -> [2|•] -> None ; tail -> [2]
enqueue 3:
  tail.next = node     [2|•] -> [3|•] -> None
  tail = node          tail -> [3]
  head -> [1] -> [2] -> [3] -> None
```

Empty-list case: there is no tail to hang off, so `head = tail = node`.

**`dequeue()` — O(1).** Detach the head, advance `head`; if that empties the
queue, reset `tail`.

```
before:  head -> [1|•] -> [2|•] -> None
dequeue:
  node = head           node -> [1]
  head = node.next      head -> [2]
  (head not None, leave tail)
  return node.value     -> 1
```

If `head` is `None` on entry, return `None` (empty queue — no exception). If
after advancing `head is None`, you **must** set `tail = None` too, or the next
enqueue corrupts the queue (see edge cases).

**`peek()` — O(1).** Return `head.value` if `head` exists, else `None`. No
mutation.

```python
def peek(self):
    return self.head.value if self.head is not None else None
```

## Complexity, derived

| Operation | Time | Why |
|-----------|------|-----|
| `enqueue` | O(1) | `tail` lets us append without walking. |
| `dequeue` | O(1) | Removing the head is two pointer writes. |
| `peek`    | O(1) | One field read. |
| `length`  | O(1) | Stored. |

**Why O(1) and not O(n)?** Every operation touches a *fixed* number of pointers
no matter how long the queue is. The `tail` pointer is the linchpin for
`enqueue`: without it, finding the back would mean walking from `head`, making
`enqueue` O(n). With it, both ends are direct field reads.

## Edge cases in detail

- **Enqueue after emptying must reset the tail** (`test_enqueue_after_emptying`).
  Enqueue `1`, dequeue it (queue now empty), enqueue `2`. When the dequeue
  empties the queue it must set `tail = None`. If it forgets, `tail` still points
  at the dead node `1`, so the next `enqueue` does `tail.next = node` — attaching
  `2` to a node that `head` can no longer reach. Then `peek()` returns the wrong
  value. This test exists to catch exactly that stale-tail bug.

- **Dequeue / peek on empty return `None`** (`test_empty_returns_none`). A queue
  doesn't raise when empty — it answers "nothing here" with `None`. (Contrast
  with `get(i)` on a list, which raises `IndexError`. Different contracts: an
  index is a *claim* a slot exists; dequeue is a *request* that may legitimately
  find nothing.)

- **Single element.** Enqueue one, dequeue it: `head` becomes `None`, so `tail`
  must too. The head and tail collapse together.

## Variations & trade-offs

- **Why not `list.pop(0)` for a queue?** A Python `list` is a contiguous array.
  `pop(0)` removes the front, then shifts *every* remaining element one slot left
  — that's O(n) per dequeue, O(n²) to drain the queue. The linked-list version
  keeps dequeue O(1) by just moving the `head` pointer. This is the whole reason
  the stub forbids `pop(0)`.

- **`collections.deque`.** The real-world answer: a doubly linked / block-based
  structure with O(1) `append` and `popleft`. Use it in production; build the
  linked version once to understand *why* it's O(1).

- **Ring buffer (array-backed queue).** Keep a fixed array with `front` and
  `back` indices that wrap around modulo capacity. O(1) ends *and* cache-friendly
  contiguous memory, at the cost of a fixed capacity (or amortized resizing).
  Trades the linked list's flexibility for locality.

- **Two-stack queue.** A classic puzzle: implement a queue from two stacks,
  giving amortized O(1) dequeue. Good for understanding amortization.

## Connections

- A queue is the engine of **breadth-first search**. BFS visits nodes in waves
  by enqueuing neighbors and dequeuing in FIFO order — see
  [tree BFS](../trees/bt_bfs.md) and
  [graph BFS](../graphs/bfs_graph_matrix.md). Swap the queue for a stack and BFS
  becomes DFS; the data structure *is* the traversal order.
- Internally it's a [singly linked list](../linked_lists/singly_linked_list.deep.md)
  restricted to head-remove + tail-append.
- Its mirror twin is the [Stack](stack.deep.md) — same nodes, opposite end.

## Self-check

1. Which field is the front and which is the back, and why does that assignment
   make the structure FIFO rather than LIFO?
2. Why must `dequeue` reset `tail = None` when it empties the queue? What
   concrete failure does `test_enqueue_after_emptying` trigger if you don't?
3. Why is `enqueue` O(1) here but O(n) without a `tail` pointer?
4. Why does `dequeue` return `None` on empty instead of raising?
5. Why is a Python-`list`-with-`pop(0)` queue O(n) per dequeue?
6. How would you turn this exact code into a stack? What single change?

## Deep dive: common bugs

- **Stale tail after emptying.** The #1 queue bug: forgetting `tail = None` in
  `dequeue` when `head` becomes `None`. The queue *looks* empty (`head is None`)
  but `tail` points at a ghost, and the next `enqueue` builds a detached chain.
  `test_enqueue_after_emptying` is the tripwire.

- **Losing the rest of the queue.** In `dequeue`, read `node.next` into `head`
  *before* you let `node` go. Overwriting in the wrong order can drop the
  remaining elements.

- **Forgetting `length`.** `enqueue` must `+= 1`, `dequeue` must `-= 1`. A
  drifting count makes any `length`-based logic lie.

- **Using truthiness for emptiness.** Check `head is None`, not `if not head` or
  `if not length` when values might be falsy — though here emptiness keys off the
  head pointer, the habit matters (see the ArrayList deep dive for where this
  bites hard).

- **Dequeuing from the tail.** Removing from the wrong end silently turns your
  queue into a stack. The tests' FIFO order assertion catches it.
