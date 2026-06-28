# Doubly Linked List

> linked_lists · stub: `src/topics/linked_lists/doubly_linked_list.py` · test: `tests/test_doubly_linked_list.py`
>
> 📚 Need more detail? See the [in-depth version](doubly_linked_list.deep.md).

## Intuition

A doubly linked list is a singly linked list with a second arrow on every node:
each box knows both the box *after* it (`next`) and the box *before* it (`prev`).
That backward arrow means you can walk in either direction and, crucially, remove
a node in O(1) once you're holding it — you no longer have to hunt for its
predecessor. Think of a **conga line** where each dancer holds the shoulders of
the person in front *and* feels the hands of the person behind.

## How it works

Same public interface as the singly list (`head`, `tail`, `length`), but each
node has three fields: `prev`, `value`, `next`. The head's `prev` is `None` and
the tail's `next` is `None`.

```
None <- [1] <-> [2] <-> [3] -> None
        ^head                ^tail
```

**append(4)** — link both directions, then move tail:

```
[3] <-> [4]     node.prev = tail; tail.next = node; tail = node
```

**insert_at(item, 2)** into `[1] <-> [2] <-> [3]` — find the node currently at
index 2 (call it `cur`), grab `cur.prev`, and splice the new node between them by
fixing **four** pointers:

```
before:  [1] <-> [2] <----------> [3]
                  prev            cur
after:   [1] <-> [2] <-> [X] <-> [3]
   node.prev = prev   node.next = cur
   prev.next = node   cur.prev = node
```

**remove_at / remove** — the payoff. Given the node itself, bridge its neighbours:

```
prev.next = node.next        # forward arrow skips the node
node.next.prev = node.prev   # backward arrow skips it too
```

When `node.prev is None` you removed the head (update `head`); when
`node.next is None` you removed the tail (update `tail`). A shared `_remove_node`
helper handles all four positions. Bonus: `_node_at` can walk from whichever end
is closer, halving the average traversal.

## Complexity

| Operation     | Big-O  | Why                                       |
| ------------- | ------ | ----------------------------------------- |
| `prepend`     | O(1)   | re-point head + one `prev`                |
| `append`      | O(1)   | re-point tail + one `prev`                |
| `get`         | O(n)   | walk (from nearer end)                    |
| `insert_at`   | O(n)   | O(n) to walk, O(1) to relink              |
| `remove_at`   | O(n)   | O(n) to find, O(1) to unlink              |
| `remove(val)` | O(n)   | scan until value matches                  |

- **Space:** O(n) (two pointers per node — a constant factor more than singly)

## Common pitfalls

- **Relinking only one direction.** Every insert/remove must fix *both* `next`
  and `prev` on the affected neighbours, or a later backward walk corrupts.
- **`None` neighbours at the ends.** Guard with `if node.prev is not None` /
  `if node.next is not None` before dereferencing; the `else` branch updates
  `head` or `tail`. `test_remove_at_all_positions` removes head and tail.
- **First insert into an empty list** must set *both* `head` and `tail` to the
  new node.
- **Don't reuse stale local pointers** after relinking — read `prev`/`next` into
  variables first, then rewire.
- **`remove(item)` returns `None`** when the value is absent.

## Your task

Implement the class in `src/topics/linked_lists/doubly_linked_list.py`, then run:

```bash
uv run pytest -k doubly_linked_list
```

Peek at `solutions/doubly_linked_list.py` only once you've given it a real attempt.
