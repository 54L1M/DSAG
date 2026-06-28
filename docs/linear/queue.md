# Queue (FIFO)

> linear · stub: `src/topics/linear/queue.py` · test: `tests/test_queue.py`
>
> 📚 Need more detail? See the [in-depth version](queue.deep.md).

## Intuition

A queue is **first in, first out (FIFO)**: items leave in the same order they
arrived. It is exactly the **line at a shop** — you join at the back, and the
person who has waited longest is served first. The two operations are `enqueue`
(join the back) and `dequeue` (serve the front).

## How it works

Back it with a singly linked list that tracks both ends: `head` is the front
(where you remove), `tail` is the back (where you add). Each node has `value` and
`next`. Keeping both pointers is what makes *both* operations O(1).

```
dequeue here          enqueue here
   v                       v
 head -> [1] -> [2] -> [3] <- tail
```

**enqueue(4)** — attach to the tail and advance it:

```
[3] -> [4]      tail.next = node; tail = node; length = 4
```

**dequeue()** — detach the head and advance it forward:

```
head = head.next        # front [1] removed, [2] is the new front
return old_head.value
```

**peek()** just returns `head.value` without unlinking anything.

Worked example: enqueue 1, 2, 3 → front is 1. `dequeue()` returns 1, then 2.
`peek()` now returns 3. Notice you remove from the *opposite* end you add to —
that is what gives FIFO order.

## Complexity

| Operation  | Big-O |
| ---------- | ----- |
| `enqueue`  | O(1)  |
| `dequeue`  | O(1)  |
| `peek`     | O(1)  |

- **Space:** O(n)

## Common pitfalls

- **Do not use a Python `list` with `list.pop(0)`.** That re-shifts every element
  and is O(n) — it defeats the whole point. Use linked nodes.
- **Update `tail` when the queue empties.** After `dequeue` makes `head` become
  `None`, set `tail = None` too, or the next `enqueue` will dangle off a stale
  node. `test_enqueue_after_emptying` checks this.
- **`dequeue` / `peek` on an empty queue return `None`**, not an exception.
- **Keep the ends straight:** enqueue at `tail`, dequeue at `head`. Swapping them
  silently turns your queue into a stack.
- **Maintain `length`** on every add/remove so the counter stays in sync.

## Your task

Implement the class in `src/topics/linear/queue.py`, then run:

```bash
uv run pytest -k queue
```

Peek at `solutions/queue.py` only once you've given it a real attempt.
