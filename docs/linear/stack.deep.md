# Stack (LIFO) — In Depth

> In-depth companion · linear · stub: `src/topics/linear/stack.py` · test: `tests/test_stack.py`
>
> New here? Read the [quick version](stack.md) first.

## The mental model

A stack is **last in, first out (LIFO)**: the most recently added item is the
first one out, like a pile of plates. Three operations: `push` (add on top),
`pop` (take off the top), `peek` (look at the top).

The implementation is the leanest of the linked structures: a singly linked list
where **every operation happens at the head**. The head *is* the top of the
stack. There's no `tail` pointer at all — we never need it.

```
top
 |
 v
[3|•] -> [2|•] -> [1|•] -> None
 ^push/pop/peek here
```

Pushing `3` onto `[2,1]` puts the newest node at the head; popping takes it back
off. Because both happen at the head, both are O(1). The list object holds just
`head` and `length` — note the absence of `tail`.

```python
class _Node:
    __slots__ = ("value", "next")
# Stack holds: head, length   (no tail!)
```

## Why it works — the invariant

1. **`length` equals the node count** from `head` to `None`.
2. **`head` is the top** — the most recently pushed, not-yet-popped item.
3. **Newer nodes are closer to the head.** Push always inserts at the head, so
   the chain runs newest → oldest. That ordering *is* LIFO.
4. **Empty ⟺ `head is None` ⟺ `length == 0`.**

The entire LIFO behavior comes from one decision: insert and remove at the same
end. Compare the [Queue](queue.deep.md), which removes at the *opposite* end from
where it inserts — that one choice is the whole difference between LIFO and FIFO.

## Detailed walkthrough

**`push(item)` — O(1).** New node points at the old top; head moves to it. This
is exactly `prepend` from the singly linked list.

```
before:  head -> [2|•] -> [1|•] -> None
push 3:
  node.next = head      [3|•] -> [2]
  head = node           head -> [3] -> [2] -> [1] -> None
  length += 1
```

No empty-list special case is needed: if `head` was `None`, `node.next` becomes
`None` and the new node is correctly the sole element.

**`pop()` — O(1).** Detach the head, advance `head`, return the value.

```
before:  head -> [3|•] -> [2|•] -> [1|•] -> None
pop:
  node = head           node -> [3]
  head = node.next      head -> [2]
  length -= 1
  return node.value     -> 3
```

If `head is None` on entry, return `None` — popping an empty stack is not an
error. Note there is **no `tail` to reset** (unlike the queue), which is one
fewer place to get wrong: a stack with no tail pointer simply can't have the
stale-tail bug.

**`peek()` — O(1).** Return `head.value` if it exists, else `None`.

```python
def peek(self):
    return self.head.value if self.head is not None else None
```

## Complexity, derived

| Operation | Time | Why |
|-----------|------|-----|
| `push`    | O(1) | Insert at head: two pointer writes. |
| `pop`     | O(1) | Remove at head: two pointer writes. |
| `peek`    | O(1) | One field read. |
| `length`  | O(1) | Stored. |

**Why is everything O(1)?** Because every operation touches the head and only
the head — a fixed amount of work independent of stack size. There's no walking
and no shifting. The stack is the simplest case of "always touch one end of a
linked list," which is why it's the cheapest structure here.

## Edge cases in detail

- **Pop / peek on empty return `None`** (`test_empty_returns_none`). Like the
  queue, an empty stack answers with `None`, not an exception. The contract is
  "give me the top if there is one," and "there isn't one" is a valid answer.

- **Push after emptying** (`test_push_after_emptying`). Push `1`, pop it, push
  `2`, peek. Because there's no `tail` pointer, the only state is `head` and
  `length`; after the pop `head is None`, and the next push correctly makes the
  new node the head. The stack is immune to the tail-reset bug that bites the
  queue — a nice illustration of "less state, fewer bugs."

- **Single element.** Push one, pop it: `head` becomes `None`, `length` becomes
  `0`. Nothing else to clean up.

## Variations & trade-offs

- **Array-backed stack.** You can build a stack on an [ArrayList](array_list.deep.md)
  / dynamic array: `push` is amortized O(1) (append, occasionally double), `pop`
  is O(1) (truncate). This wins on cache locality (contiguous memory) and is what
  most languages' standard stacks do. The linked version wins on worst-case
  guarantees (no occasional O(n) resize) and never wastes spare capacity.

- **Linked vs. array trade-off.** Linked: every push allocates a node (more
  memory churn, pointer-chasing on access). Array: amortized growth, but
  occasional O(n) copy and possibly unused slots. For a pure push/pop workload
  the array version is usually faster in practice.

- **Python `list` as a stack.** In real code, a Python `list` *is* an excellent
  stack: `append` and `pop()` (no argument) are both amortized O(1) at the end.
  The hand-built linked version is the teaching tool.

## Connections

- A stack is the engine of **depth-first search**. DFS dives deep by pushing
  neighbors and popping the most recent — see [graph DFS](../graphs/dfs_graph_list.md)
  and [DFS on a BST](../trees/dfs_on_bst.md). The **call stack** that powers any
  recursive traversal is literally a stack; an iterative DFS makes it explicit.
- Internally it's a [singly linked list](../linked_lists/singly_linked_list.deep.md)
  using only `prepend` + remove-head.
- Its mirror twin is the [Queue](queue.deep.md): same nodes, but the queue
  removes from the far end (FIFO) while the stack removes from the same end
  (LIFO).

## Self-check

1. Why does a stack need only a `head` pointer while a queue needs both `head`
   and `tail`?
2. Which singly-linked-list method is `push` identical to?
3. Why is the stack immune to the "stale tail after emptying" bug that the queue
   must guard against?
4. Why does `pop` return `None` on empty instead of raising?
5. What single change to the *queue's* logic would turn it into a stack?
6. Give one reason to prefer an array-backed stack and one reason to prefer the
   linked version.

## Deep dive: common bugs

- **Losing the rest of the stack.** In `pop`, capture `node.next` into `head`
  before discarding `node`. Reassigning in the wrong order can drop everything
  under the top.

- **Forgetting `length`.** `push` must `+= 1`, `pop` must `-= 1`. A wrong count
  silently breaks any size-dependent logic built on top.

- **Raising instead of returning `None` on empty.** The contract here is to
  return `None`; raising would break `test_empty_returns_none`.

- **Adding an unnecessary `tail`.** Some learners copy the queue and keep a
  `tail`. It's dead weight for a stack and just another field to keep in sync —
  resist it.

- **Using truthiness for emptiness.** Check `head is None`, not `if not head`.
  This habit matters most where stored values can be falsy (see the
  [ArrayList deep dive](array_list.deep.md)); building it everywhere keeps you
  safe.
