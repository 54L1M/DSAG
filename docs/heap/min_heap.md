# Min Heap (Array-Backed Binary Heap)

> heap · stub: `src/topics/heap/min_heap.py` · test: `tests/test_min_heap.py`
>
> 📚 Need more detail? See the [in-depth version](min_heap.deep.md).

## Intuition
A min heap always lets you grab the *smallest* element instantly, while keeping
inserts and removals cheap. Picture a tournament bracket flipped upside down: the
single overall winner (the smallest value) sits at the top, and every parent is
smaller than its children. We don't fully sort everything — we just keep enough
order that the minimum is always at the root.

The clever part: a *complete* binary tree fits perfectly into a flat array, so we
need no node objects or pointers at all.

## How it works
Store the tree level-by-level in a list `data`. For the node at index `i`:
- parent = `(i - 1) // 2`
- left child = `2 * i + 1`
- right child = `2 * i + 2`

```
        1            index:  0  1  2  3  4  5
       / \           data : [1, 3, 2, 5, 9, 8]
      3   2
     / \   \         data[0]=1 is the root (min)
    5   9   8        data[1]=3, its children are data[3]=5, data[4]=9
```

**`insert(value)` — append, then bubble up.**
Add at the end (keeps the tree complete), `length += 1`, then swap upward while the
value is smaller than its parent. Insert `0` into the heap above:
```
append:  [1, 3, 2, 5, 9, 8, 0]      idx 6, parent (6-1)//2 = 2 -> data[2]=2
0 < 2 -> swap:  [1, 3, 0, 5, 9, 8, 2]   idx 2, parent 0 -> data[0]=1
0 < 1 -> swap:  [0, 3, 1, 5, 9, 8, 2]   idx 0 -> stop. New min is 0.
```

**`delete()` — pop the min, move last to root, bubble down.**
The root is the answer. Decrement `length`, pop the *last* element, place it at
index 0, then swap it downward with its **smaller** child until it's in order.
From `[1, 3, 2, 5, 9, 8]`:
```
top = 1. pop last (8), put at root: [8, 3, 2, 5, 9]
idx 0: children 3 (idx1) and 2 (idx2); smaller is 2 -> swap: [2, 3, 8, 5, 9]
idx 2: children would be idx5,6 (out of range) -> stop. Return 1.
```
Repeating `delete` yields values in sorted order — that's the heapsort idea, and
exactly what `test_pops_in_sorted_order` checks.

## Complexity
| Operation | Big-O |
|-----------|-------|
| `insert`  | O(log n) |
| `delete`  | O(log n) |
| peek min (`data[0]`) | O(1) |

Height of the tree is `log n`, and bubbling travels at most one full height.
- **Space:** O(n)

## Common pitfalls
- **Index math:** parent is `(i-1)//2`; children are `2i+1` / `2i+2`. A single
  off-by-one breaks ordering subtly.
- **delete order of steps:** you must move the *last* element to the root *before*
  bubbling down. Skipping that (or bubbling the wrong node) corrupts the heap.
- **Bubble down to the SMALLER child:** comparing against only the left child, or
  the larger child, lets a bigger value sit above a smaller one.
- **Empty / single element:** `delete` on an empty heap returns `None`; after
  popping the last element there's nothing left to bubble.
- **Length vs len(data):** bubble-down bounds must use `self.length`, not stale
  indices, or you'll read elements you logically removed.

## Your task
Implement the class in `src/topics/heap/min_heap.py`, then run:

```bash
uv run pytest -k min_heap
```

Peek at `solutions/min_heap.py` only once you've given it a real attempt.
