# Maze Solver — In Depth

> In-depth companion · recursion · stub: `src/topics/recursion/maze_solver.py` · test: `tests/test_maze_solver.py`
>
> New here? Read the [quick version](maze_solver.md) first.

## The mental model

Forget the grid for a second and picture a person standing in a cell holding a
ball of string. The rule they follow is mechanical: "Try to step in a direction.
If that step eventually reaches the exit, great — I'm part of the answer. If it
turns out to be hopeless, reel the string back to me and try the next
direction."

That single rule, applied recursively, *is* the algorithm. The clever part is
that you never write a loop that manages "where have I been" or "how do I undo a
wrong turn." The **call stack does the bookkeeping for you**:

- Each active recursive call is one person standing in one cell.
- The chain of callers — `solve` called `walk((0,0))`, which called
  `walk((1,0))`, which called `walk((2,0))`, ... — is literally the route walked
  so far. The stack of frames mirrors the line of string.
- Returning `False` from a call is "reel the string back one step."
- Returning `True` is "the exit is reachable from here," and it propagates all
  the way up, freezing the path in place.

So when you read `_walk`, read it as: *"Am I a valid place to stand? If I'm the
exit, done. Otherwise, does any neighbour lead to the exit?"* The whole maze is
solved by one cell repeatedly asking its four neighbours the same question.

## Why it works — the invariant

The function is built around one promise, and every line either upholds it or
relies on it:

> **Invariant:** when `_walk(curr)` returns `True`, the shared `path` list ends
> with a contiguous, repeat-free walk from the original `start` up to and
> including `end`. When it returns `False`, `path` is exactly what it was when
> the call began (the call left no trace).

Why each piece is needed to keep that promise true:

- **`seen` guarantees termination and the "repeat-free" clause.** The grid is
  finite, and a cell is marked `seen` the instant we stand on it and never
  un-marked. So no cell is ever entered twice. Every recursive call therefore
  consumes one fresh cell; with a finite supply, the recursion must bottom out.
  Without `seen`, `(0,0) -> (1,0) -> (0,0) -> (1,0) -> ...` recurses forever.
- **`path.append` on entry + `path.pop` on the failing exit keeps the
  "leaves no trace" half.** If a cell appends itself but every direction fails,
  it must remove itself before returning `False`, or the caller's `path` would
  be polluted with a dead-end cell. The success path deliberately does *not*
  pop — that's how the winning cells stay in the list.
- **The `end` check sits after `append`**, so the final cell is included, and a
  zero-length search (`start == end`) still records the one cell.

Backtracking is just "restore the invariant before returning failure." Once you
see `pop()` as the mirror image of `append()`, the structure is symmetric.

## Detailed walkthrough

Signature and contract: `solve(maze, wall, start, end) -> list[Point]`. A
`Point` is `(row, col)` (see `common/types.py`). It returns the path inclusive
of both endpoints, or `[]` when no path exists.

```python
_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right

def solve(maze, wall, start, end):
    if not maze:
        return []
    seen = [[False] * len(row) for row in maze]     # one bool per cell
    path = []
    if _walk(maze, wall, start, end, seen, path):
        return path
    return []
```

`solve` only sets up the shared mutable state — the `seen` grid and the `path`
accumulator — then delegates to `_walk`. Both are passed by reference, so every
recursive frame reads and writes the *same* two objects.

```python
def _walk(maze, wall, curr, end, seen, path):
    r, c = curr
    if r < 0 or r >= len(maze) or c < 0 or c >= len(maze[r]):   # (1) off-grid
        return False
    if maze[r][c] == wall or seen[r][c]:                        # (2) wall/seen
        return False
    seen[r][c] = True                                           # (3) mark
    path.append(curr)                                           # (4) record
    if curr == end:                                            # (5) success
        return True
    for dr, dc in _DIRECTIONS:                                  # (6) recurse
        if _walk(maze, wall, (r + dr, c + dc), end, seen, path):
            return True
    path.pop()                                                  # (7) backtrack
    return False
```

The **order of the base cases is load-bearing**. Off-grid is tested *first*, so
that by the time we evaluate `maze[r][c]` in step (2) we already know `r` and `c`
are in range. Flip them and a neighbour at `(-1, 0)` indexes `maze[-1]`, which in
Python silently wraps to the last row instead of failing — a subtle, wrong
answer rather than a crash.

Note also what is *not* here: the maze itself is never mutated. Visited state
lives entirely in the separate `seen` grid, so the input strings stay pristine
(and `maze` rows are immutable strings anyway).

## Full ASCII trace on the 4x4 test maze

The maze from `test_finds_a_valid_path`, with `start=(0,0)`, `end=(2,3)`:

```
       col 0 1 2 3
row 0    . . . .
row 1    . # # .
row 2    . # . .
row 3    . . . #     wall = '#'
```

Directions are tried in order up, down, left, right. Watch the stack grow (each
indent level is a live frame / one cell of string), and watch one real
backtrack:

```
solve -> _walk(0,0)
  append (0,0); not end. try up (-1,0) -> off-grid ✗
                try down (1,0):
    _walk(1,0): append (1,0); not end. up (0,0) seen ✗
                down (2,0):
      _walk(2,0): append (2,0); not end. up (1,0) seen ✗
                  down (3,0):
        _walk(3,0): append (3,0); not end. up (2,0) seen ✗
                    down (4,0) off-grid ✗; left (3,-1) off-grid ✗
                    right (3,1):
          _walk(3,1): append (3,1); not end. up (2,1)='#' ✗
                      down (4,1) off-grid ✗; left (3,0) seen ✗
                      right (3,2):
            _walk(3,2): append (3,2); not end. up (2,2):
              _walk(2,2): append (2,2); not end. up (1,2)='#' ✗
                          down (3,2) seen ✗; left (2,1)='#' ✗
                          right (2,3):
                _walk(2,3): append (2,3); curr == end -> return True ✓
              returns True ✓   (no pop — this cell is in the answer)
            returns True ✓
          returns True ✓
        returns True ✓        every frame short-circuits up the chain
      returns True ✓
    returns True ✓
  returns True ✓
solve sees True -> returns path
```

Final path: `[(0,0),(1,0),(2,0),(3,0),(3,1),(3,2),(2,2),(2,3)]`.

A backtrack with a real `pop()` is easy to see if you imagine the bottom row
were blocked. Suppose `(3,1)` had failed all four directions: it would hit
`path.pop()`, removing `(3,1)`, and return `False` to `(3,0)`, whose string is
now reeled back — `(3,0)` would then try its remaining directions. That pop is
what keeps a dead-end cell out of the final list.

## Complexity, derived

**Time — O(rows · cols).** The argument hinges on `seen`. A cell can only pass
base cases (1) and (2) once: the first time it's reached it is marked, and every
later attempt to enter it fails the `seen[r][c]` test in O(1). So the body past
step (3) runs at most once per cell. Each such body does O(4) constant work (the
four-direction loop). Total work is therefore proportional to the number of
cells, `rows · cols`. The repeated O(1) "bounce off a seen/wall cell" attempts
are also bounded by 4 per cell, so they don't change the order.

**Space — O(rows · cols), in two parts:**

- The `seen` grid is exactly `rows · cols` booleans.
- The recursion stack is at most the length of the current path, which is at most
  the number of cells (a path can't repeat). In a long snake-like corridor the
  depth genuinely approaches `rows · cols`.

Both terms are O(rows · cols), so the total is too.

## Edge cases in detail

- **No path → `[]`.** In `test_no_path_returns_empty`, a wall column splits the
  maze. The recursion explores the whole left region, every branch dead-ends and
  pops, the top call returns `False`, and `solve` returns `[]` (not `None`).
- **`start == end` → `[(0,0)]`.** Covered by `test_start_equals_end`. Because the
  `curr == end` check happens *after* `append`, the start cell is recorded and we
  return `True` immediately with a single-element path.
- **`start` on a wall, or `end` unreachable behind walls.** A wall `start` fails
  base case (2) on the very first call → `[]`. An end walled off is found
  unreachable after exhausting the reachable region.
- **Empty maze (`maze == []`).** Guarded explicitly in `solve` before building
  `seen`, returning `[]`.
- **Walls everywhere except start.** First call marks start, all four neighbours
  are walls/off-grid, the start cell pops, top returns `False` → `[]` (unless
  start happens to equal end).
- **Ragged rows.** Step (1) checks `c >= len(maze[r])` per-row rather than
  against a single width, so it stays safe even if rows differed in length.

## Variations & trade-offs

- **DFS path is not the shortest.** This recursion commits to the first
  direction that "works" and only reconsiders on failure, so it returns *a* path,
  not the shortest one. For the shortest path, use **BFS**: a queue of cells, a
  `parent`/`prev` map recording who discovered each cell, expand cells in
  distance order, and when you pop `end`, reconstruct the path by walking
  `parent` links backward. BFS visits cells in rings of increasing distance, so
  the first time it reaches `end` is along a shortest route. Same O(rows · cols)
  time; the trade is a queue and a parent map instead of the call stack.
- **Explicit stack instead of recursion.** You can convert the DFS to an
  iterative loop using your own `list` as a stack of cells to visit. This sidesteps
  Python's recursion limit but you lose the "free" path bookkeeping — you have to
  reconstruct the path yourself (again via a parent map), because an explicit
  stack of *to-visit* cells is not the same as the *current path*.
- **Recursion-limit concerns.** Python's default limit (~1000 frames) means a
  maze with a reachable path longer than ~1000 cells can raise
  `RecursionError`. A 40×40 fully-open maze can have a path that long. Options:
  raise the limit with `sys.setrecursionlimit`, or switch to the iterative form.
- **Un-marking on backtrack.** Some maze variants un-set `seen` when backtracking
  so cells can be reused by other paths (needed when enumerating *all* paths).
  Here we only need *one* path, so leaving `seen` set is both correct and what
  keeps the algorithm linear.

## Connections

- **`../graphs/dfs_graph_list.md`** — this *is* depth-first search. A grid is just
  an implicit graph: each cell is a node, and its (up to four) walkable neighbours
  are its edges. The graph DFS uses an explicit adjacency list and a `seen` set;
  here the neighbours are computed on the fly from `_DIRECTIONS`. Same traversal,
  different graph representation.
- **`../linear/stack.md`** — the call stack is a stack. The iterative variant
  above makes that stack explicit. Understanding push/pop there is exactly
  understanding `append`/`pop` here.

## Self-check

1. Why does checking off-grid *before* `maze[r][c]` matter in Python
   specifically? (Hint: what does `maze[-1]` do?)
2. The success path does not call `path.pop()`, but the failure path does.
   Explain why this asymmetry is correct in terms of the invariant.
3. If you removed `seen` entirely, what concrete bad behaviour happens on the
   4×4 test maze, and why?
4. The returned path isn't guaranteed to be the shortest. Sketch what you'd
   change to get the shortest path, and what new data structures you'd need.
5. For a 5×5 fully-open maze, what is the maximum recursion depth this can reach,
   and which input shape maximizes it?
6. Suppose you forgot the `path.pop()` line. Construct a small maze where the
   returned list is no longer a contiguous walk, and trace why.

## Deep dive: common bugs

- **Wrong base-case order.** Testing `maze[r][c] == wall` before the off-grid
  guard. With a neighbour like `(-1, 0)`, `maze[-1]` wraps to the bottom row in
  Python — no exception, just a quietly wrong answer where the search "teleports"
  across the maze. Always range-check first.
- **Forgetting to mark `seen` (infinite recursion / test timeout).** If you don't
  set `seen[r][c] = True`, two adjacent open cells call each other forever:
  `(0,0) -> (1,0) -> (0,0) -> ...`. In the test suite this manifests as a hang or
  `RecursionError`, not a clean failure. Mark the cell the moment you stand on it,
  before recursing.
- **Not backtracking.** Skipping `path.pop()` on dead ends leaves cells from
  abandoned branches in `path`. The endpoints might still be right, but
  `_valid_path` in the test checks that consecutive entries are orthogonal
  neighbours; a leftover dead-end cell breaks that adjacency and the test fails.
- **Mutating the maze instead of using a `seen` grid.** Writing a visited marker
  back into `maze[r][c]` fails because the rows are immutable `str` objects
  (`TypeError`), and even if you converted them to lists it would corrupt the
  input and conflate "wall" with "visited." Keep visited state in a separate
  `seen` structure.
