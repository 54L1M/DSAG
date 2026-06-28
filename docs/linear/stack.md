# Stack (LIFO)

> linear · stub: `src/topics/linear/stack.py` · test: `tests/test_stack.py`
>
> 📚 Need more detail? See the [in-depth version](stack.deep.md).

## Intuition

A stack is **last in, first out (LIFO)**: the most recently added item is the
first one out. Picture a **pile of plates** — you add a plate on top and you take
the next plate off the top; you never pull one from the bottom. The operations
are `push` (add on top), `pop` (take off the top), and `peek` (look at the top).

## How it works

Back it with a singly linked list and a single `head` pointer that always points
at the **top** of the stack. Every operation happens at the head, so all three
are O(1) — you never walk the list and never need a tail pointer.

```
top
 v
head -> [3] -> [2] -> [1] -> None
```

**push(item)** — new node points at the old top, then becomes the top:

```
node.next = head        # [4] -> [3] -> ...
head = node
```

**pop()** — detach the top and step the head down:

```
head = head.next        # top [4] removed, [3] is the new top
return old_head.value
```

**peek()** returns `head.value` without unlinking.

Worked example: push 1, 2, 3 → top is 3. `peek()` returns 3. `pop()` returns 3,
then `pop()` returns 2. Compare with a queue: same linked nodes, but a stack adds
*and* removes at the **same** end, which flips the order to LIFO.

## Complexity

| Operation | Big-O |
| --------- | ----- |
| `push`    | O(1)  |
| `pop`     | O(1)  |
| `peek`    | O(1)  |

- **Space:** O(n)

## Common pitfalls

- **Push and pop must use the *same* end (the head).** Adding at one end and
  removing at the other gives FIFO (a queue), not LIFO.
- **`pop` / `peek` on an empty stack return `None`**, not an exception.
- **Set `node.next = head` *before* reassigning `head`**, or you lose the rest of
  the stack.
- **Keep `length` in sync** on every push/pop.
- No tail pointer is needed here — if you find yourself walking the list, you've
  over-engineered it.

## Your task

Implement the class in `src/topics/linear/stack.py`, then run:

```bash
uv run pytest -k stack
```

Peek at `solutions/stack.py` only once you've given it a real attempt.
