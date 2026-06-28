# Maze Solver

> recursion · stub: `src/topics/recursion/maze_solver.py` · test: `tests/test_maze_solver.py`
>
> 📚 Need more detail? See the [in-depth version](maze_solver.deep.md).

## Intuition

You drop into a maze and want a route from `start` to `end`. The simplest mental
move: "from where I stand, try a direction; if that leads to a dead end, step
back and try another." That "step back and try another" is **backtracking**.
It's like exploring a corn maze with a ball of string — you unspool as you walk,
and reel it back in whenever you hit a wall, until one path reaches the exit.

## How it works

The contract is `solve(maze, wall, start, end) -> list[Point]`, where a `Point`
is a `(row, col)` tuple and `maze` is a list of equal-length strings. A cell
equal to `wall` is blocked; anything else is walkable. You return the path
inclusive of both ends, or `[]` if none exists.

A recursive helper `walk(curr)` does the work, carrying a `seen` grid (visited
marks) and the `path` so far:

1. **Base case — off the grid.** If `curr`'s row/col is outside the maze,
   return `False` (failure). Check this *first* so the next checks never index
   out of bounds.
2. **Base case — wall or already seen.** If `maze[r][c] == wall`, or we already
   visited this cell, return `False`.
3. **Mark and record.** Set `seen[r][c] = True` and append `curr` to `path`.
4. **Base case — success.** If `curr == end`, return `True`. The path is
   complete.
5. **Recurse in 4 directions.** Try up, down, left, right:
   `(-1,0), (1,0), (0,-1), (0,1)`. If any recursive call returns `True`,
   bubble `True` up immediately.
6. **Backtrack.** If all four directions failed, this cell is a dead end:
   `path.pop()` to remove it, then return `False`.

Marking `seen` is what stops you from walking in circles forever. Note we do
**not** un-mark on backtrack here — once a cell is proven useless for *this*
search, revisiting it can't help.

### Trace a small maze

```
       col 0 1 2 3
row 0    . . . .
row 1    . # # .
row 2    . # . .      start = (0,0)   end = (2,3)
row 3    . . . #      wall  = '#'
```

One successful exploration (directions tried in order up/down/left/right):

```
(0,0) -> down (1,0) -> down (2,0) -> down (3,0) -> down off-grid ✗
                                            -> right (3,1) -> right (3,2) ✓
(3,2) -> up (2,2) -> up (1,2)='#' ✗ -> right (2,3) == end ✓
```

Final path (one valid answer): `[(0,0),(1,0),(2,0),(3,0),(3,1),(3,2),(2,2),(2,3)]`.

Tests only require a *valid* contiguous walk (no repeats, orthogonal steps,
correct endpoints), so any legal route passes.

## Complexity

- **Time:** O(rows * cols)
- **Space:** O(rows * cols)

Each cell is marked `seen` at most once, so it's visited a constant number of
times; the `seen` grid plus the recursion stack are both bounded by the cell
count.

## Common pitfalls

- **Forgetting to mark `seen`** turns the search into infinite ping-pong between
  two cells. Mark a cell the moment you step on it.
- **Base-case order matters.** Check off-grid *before* indexing `maze[r][c]`, or
  a negative/oversized index will crash or silently wrap.
- **Not backtracking.** If you never `path.pop()` on a dead end, your path keeps
  cells from abandoned branches and fails the "contiguous walk" check.
- **start == end.** A single cell is a valid path of length 1 — make sure the
  success check happens after appending `curr`, so you return `[(r,c)]`.
- **Returning the wrong empty value.** No path means return `[]`, not `None`.

## Your task

Implement in `src/topics/recursion/maze_solver.py`, then run:

```bash
uv run pytest -k maze_solver
```

Peek at `solutions/maze_solver.py` only once you've given it a real attempt.
