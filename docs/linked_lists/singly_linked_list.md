# Singly Linked List

> linked_lists · stub: `src/topics/linked_lists/singly_linked_list.py` · test: `tests/test_singly_linked_list.py`
>
> 📚 Need more detail? See the [in-depth version](singly_linked_list.deep.md).

## Intuition

A singly linked list stores each value in its own little box (a *node*), and each
box holds one arrow (`next`) pointing to the box after it. Instead of sitting in
one contiguous block of memory like an array, the boxes can live anywhere — the
arrows hold the order together. Think of a **treasure hunt**: each clue tells you
where the next clue is, but you can only ever move forward, never back.

## How it works

You keep two references: `head` (the first node) and `tail` (the last node), plus
a `length` counter. Each node has `value` and `next`; the last node's `next` is
`None`. The tail pointer is what makes `append` O(1) instead of O(n).

```
head -> [1|*] -> [2|*] -> [3|/] <- tail        (* = next pointer, / = None)
```

**append(4)** — make a node, hang it off the old tail, move tail:

```
[3|*] -> [4|/]      tail.next = node; tail = node; length = 4
```

**prepend(0)** — new node points at the old head, then becomes the head:

```
[0|*] -> [1] ...    node.next = head; head = node
```

**remove_at(1)** on `[1] -> [2] -> [3]` — walk to the node *before* the target
(index 0), then "skip over" the victim by re-pointing its `next`:

```
before: [1|*] -> [2|*] -> [3]
after:  [1|------------>] [3]    prev.next = prev.next.next   (node 2 is gone)
```

Because you can only move forward, reaching index `i` means starting at `head` and
following `next` `i` times. A `_node_at` helper that does this walk keeps `get`,
`insert_at`, and `remove_at` tidy.

## Complexity

| Operation     | Big-O  | Why                                  |
| ------------- | ------ | ------------------------------------ |
| `prepend`     | O(1)   | just re-point head                   |
| `append`      | O(1)   | tail pointer; no walk needed         |
| `get`         | O(n)   | walk from head                       |
| `insert_at`   | O(n)   | walk to find the spot, O(1) to link  |
| `remove_at`   | O(n)   | walk to the node before the target   |
| `remove(val)` | O(n)   | scan until value matches             |

- **Space:** O(n)

## Common pitfalls

- **Forgetting to update `tail`.** When you remove the last node, set `tail` back
  to the new last node; when the list becomes empty, set both `head` and `tail`
  to `None`. The test `test_append_after_emptying_uses_tail` checks exactly this.
- **Removing the head needs special handling** — there is no `prev` node to
  re-point, so update `head` directly.
- **Off-by-one on `insert_at`.** `index == length` is a valid append;
  `index > length` must raise `IndexError`. Walk to index `i - 1` (the node
  *before*), not `i`.
- **`remove(item)` returns `None` when nothing matches**, not an exception.
- **Losing the rest of the list.** Always read `node.next` into a variable
  *before* you overwrite any pointer, or you'll orphan the tail of the list.

## Your task

Implement the class in `src/topics/linked_lists/singly_linked_list.py`, then run:

```bash
uv run pytest -k singly_linked_list
```

Peek at `solutions/singly_linked_list.py` only once you've given it a real attempt.
