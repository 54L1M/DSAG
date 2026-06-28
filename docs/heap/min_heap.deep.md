# Min Heap — In Depth

> In-depth companion · heap · stub: `src/topics/heap/min_heap.py` · test: `tests/test_min_heap.py`
>
> New here? Read the [quick version](min_heap.md) first.

## The mental model
A min-heap is a structure with one promise: **the smallest element is always one
step away.** It does *not* keep everything sorted — that would be expensive. It
keeps just enough order that the minimum bubbles to a known spot (the root) and
stays there as you add and remove.

Two ideas combine. First, a *binary tree* where every parent is `≤` both children
(the **heap property**). That alone guarantees the global minimum sits at the very
top, because the smallest value can't be anyone's child. Second — and this is the
trick that makes it cheap — we never build actual tree nodes. We store the tree in a
**flat list**, reading it level by level, left to right.

## Why it works — the invariant
Two invariants hold at all times between operations:

1. **Shape invariant (complete tree).** The tree is *complete*: every level is full
   except possibly the last, which fills left to right with no gaps. This is exactly
   what lets a flat array represent it — index `i` maps to a fixed tree position. If
   you ever leave a hole, the index math lies.

2. **Order invariant (heap property).** For every node, `parent ≤ child`. This is
   strictly weaker than full sorting (siblings are unordered), which is why inserts
   and deletes are O(log n) instead of O(n) — we only fix one root-to-leaf path.

Together they guarantee `data[0]` is the minimum, and that the tree height is
`⌊log₂ n⌋`, bounding the work of any fix-up.

## Detailed walkthrough
The array↔tree mapping is the crux. For the node at index `i`:

```
parent(i) = (i - 1) // 2      left(i) = 2*i + 1      right(i) = 2*i + 2
```

Tree and its array, side by side:

```
            1                    index:  0  1  2  3  4  5
          /   \                  data : [ 1, 3, 2, 5, 9, 8 ]
         3     2
        / \     \                data[0]=1  root / min
       5   9     8               data[1]=3  -> children data[3]=5, data[4]=9
                                 data[2]=2  -> children data[5]=8, data[6]=(none)
```

Check the math: node `3` is at index 1, its left child is `2*1+1 = 3` (value 5),
right is `2*1+2 = 4` (value 9). Node `5` at index 3 has parent `(3-1)//2 = 1`
(value 3). It all lines up.

### insert — append, then bubble up
Append keeps the tree complete (the new slot is the next left-to-right position).
Then restore the order invariant by swapping the newcomer upward while it is
smaller than its parent. Insert `0`:

```
append 0:        [1, 3, 2, 5, 9, 8, 0]   idx 6, parent (6-1)//2 = 2 -> data[2]=2
0 < 2  swap:     [1, 3, 0, 5, 9, 8, 2]   idx 2, parent (2-1)//2 = 0 -> data[0]=1
0 < 1  swap:     [0, 3, 1, 5, 9, 8, 2]   idx 0 -> top reached, stop
```

The new minimum `0` climbed exactly one root-to-leaf path: at most `log n` swaps.

### delete — save root, move last to root, bubble down
The answer is `data[0]`. To remove it without leaving a hole at the top, move the
**last** element into the root slot (the last slot is the only one we can drop
without breaking completeness), then push it down, always swapping with the
**smaller** child until both children are `≥` it. From `[1, 3, 2, 5, 9, 8]`:

```
save top = 1
pop last (8), place at root:   [8, 3, 2, 5, 9]      length now 5
idx 0: left=3 (idx1), right=2 (idx2); smaller child = 2
8 > 2  swap:                    [2, 3, 8, 5, 9]
idx 2: left=2*2+1=5 -> out of range (>= length); no children; stop
return 1
```

Why the *smaller* child? You're trying to make the parent the smallest of the
trio. Swapping with the larger child could leave the larger sitting above the
smaller, violating the order invariant on the other branch.

Reference shape of the two helpers:

```python
def _bubble_up(self, idx):
    while idx > 0:
        parent = (idx - 1) // 2
        if self.data[idx] >= self.data[parent]:
            break
        self.data[idx], self.data[parent] = self.data[parent], self.data[idx]
        idx = parent

def _bubble_down(self, idx):
    while True:
        l, r = 2*idx + 1, 2*idx + 2
        smallest = idx
        if l < self.length and self.data[l] < self.data[smallest]: smallest = l
        if r < self.length and self.data[r] < self.data[smallest]: smallest = r
        if smallest == idx: break
        self.data[idx], self.data[smallest] = self.data[smallest], self.data[idx]
        idx = smallest
```

Note the `< self.length` guards: they are how you avoid reading past the live part
of the array.

## Complexity, derived
A complete binary tree of `n` nodes has height `h = ⌊log₂ n⌋`, because level `k`
holds up to `2^k` nodes and `1 + 2 + 4 + ... + 2^h = 2^(h+1) - 1 ≥ n`.

- **insert**: one append (amortized O(1)) plus bubble-up, which moves up one level
  per swap — at most `h` swaps. So **O(log n)**.
- **delete**: one pop plus bubble-down, at most `h` swaps down. So **O(log n)**.
- **peek** (`data[0]`): **O(1)**.

**Build-heap aside.** Inserting `n` items one by one is `O(n log n)`. But if you
already hold all `n` values, you can *heapify in O(n)*: bubble down every node from
the last parent up to the root. The cost looks like `n log n` but isn't — most
nodes are near the bottom with tiny subtrees, and the sum
`Σ (nodes at depth d) × (height below d)` converges to `O(n)`. Python's
`heapq.heapify` does exactly this.

| Operation | Big-O |
|-----------|-------|
| insert | O(log n) |
| delete | O(log n) |
| peek   | O(1) |
| build from list | O(n) heapify |

## Edge cases in detail
- **Empty delete** (`test_empty_delete_returns_none`): `length == 0` returns `None`
  before touching `data`.
- **Single element**: `delete` saves it, pops it, and since `length` is now 0 it
  skips the move-to-root / bubble-down entirely — nothing left to fix.
- **Duplicates**: `5, 5, 5` is fine. `>=` in bubble-up and `<` in bubble-down treat
  equal values as already-ordered, so equal keys never thrash.
- **Interleaved insert/delete** (`test_interleaved_insert_delete`): the heap stays
  valid no matter how you mix operations; each delete returns the current minimum.
- **Repeated delete = sorted order** (`test_pops_in_sorted_order`,
  `test_random_matches_sorted`): popping until empty yields ascending order. That's
  heapsort.

## Variations & trade-offs
- **Max-heap**: flip every comparison (`<` ↔ `>`). Now the *maximum* sits at the
  root. A common Python hack for a max-heap with `heapq` is to negate values.
- **Python's `heapq`**: functions on a plain list (`heappush`, `heappop`,
  `heapify`) implementing exactly this min-heap. Building your own is the lesson;
  reach for `heapq` in real code.
- **Heapsort**: heapify in O(n), then pop `n` times at O(log n) each → O(n log n),
  in-place, not stable. Compared to `../sorting/quick_sort.md`: quicksort is usually
  faster in practice (cache-friendly) but has an O(n²) worst case; heapsort is a
  rock-solid O(n log n) worst case.
- **Heap vs sorted list as a priority queue**: a sorted list gives O(1) min but
  O(n) insert (you must shift to keep order). A heap gives O(log n) insert *and*
  O(log n) extract-min — far better when both happen often, which is the whole point
  of a priority queue.

## Connections
- `../graphs/dijkstra.md` and `../graphs/prim.md` — both use a min-heap as the
  priority queue that always serves the next-closest / cheapest node. The heap is
  literally why these run in `O(E log V)`.
- `../sorting/quick_sort.md` — heapsort is the heap-based sort; compare its
  guaranteed `O(n log n)` against quicksort's average-vs-worst behavior.

## Self-check
1. Given index 4, what are its parent, left child, and right child indices?
2. Why must `delete` move the *last* element to the root rather than, say, the
   second element?
3. Why bubble down toward the *smaller* child and not the larger?
4. The order invariant says parent ≤ children but says nothing about siblings. Why
   is that enough to guarantee `data[0]` is the global minimum?
5. Derive the height of a complete tree with `n` nodes, and explain why that bounds
   insert/delete at O(log n).
6. Building a heap by `n` inserts is O(n log n) but `heapify` is O(n). What about
   the tree's shape makes heapify cheaper?

## Deep dive: common bugs
- **Wrong index math.** `2*i` instead of `2*i+1` for the left child, or `i//2`
  instead of `(i-1)//2` for the parent. These corrupt the order invariant subtly —
  small heaps may still pass by luck, which is why the random test exists.
- **Skipping move-last-to-root.** Bubbling down from a root you never refilled
  leaves the old (already-returned) value or a gap up top. Always: save root → pop
  last → place at root → bubble down (only if `length > 0`).
- **Bubbling toward the larger child.** Compare against *both* children and pick the
  smaller before swapping. Comparing only the left child, or picking the larger,
  lets a big value sit above a smaller one.
- **`length` vs `len(data)`.** After decrementing `length` and popping, the bubble-
  down bound must be `self.length`. Using `len(self.data)` (or a stale value) can
  read elements you logically removed, or skip live ones.
- **Off-by-one in the child guard.** It's `l < self.length`, not `l <= self.length`
  — index `length` is one past the last live element.
- **Forgetting to update `length` on insert.** Then bubble-up/down see the wrong
  size and the next delete misbehaves. Increment on insert, decrement on delete,
  every time.
