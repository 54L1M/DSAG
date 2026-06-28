# Two Crystal Balls

> search · stub: `src/topics/search/two_crystal_balls.py` · test: `tests/test_two_crystal_balls.py`
>
> 📚 Need more detail? See the [in-depth version](two_crystal_balls.deep.md).

## Intuition
You have two identical crystal balls and a building. From some floor up, a dropped ball always breaks; below it, never. You want the lowest breaking floor — but you only get **two** balls, so you can't binary-search (one wrong guess too high wastes a ball). The trick: with the first ball take big jumps of √n floors to find the *region* where it breaks, then with the second ball walk that small region one floor at a time. The input here is a boolean list `breaks` that's `False...False, True...True`; you return the index of the first `True`, or `-1`.

## How it works
Let `n = len(breaks)` and `jump = √n` (at least 1).

1. If the list is empty, return `-1`.
2. **Big jumps (first ball):** check `breaks[jump]`, `breaks[2*jump]`, … until you find a `True` or run off the end. This locates a window of size ~`jump` known to contain the first `True`.
3. **Linear walk (second ball):** step back to the start of that window (`i -= jump`) and scan forward up to `jump + 1` positions.
4. Return the first index where `breaks[i]` is `True`; if none is found, return `-1`.

Worked example — `n = 16`, first `True` at index `9`, so `jump = 4`:

| phase      | check index | breaks? | action                  |
|------------|-------------|---------|-------------------------|
| jump       | 4           | False   | jump again              |
| jump       | 8           | False   | jump again              |
| jump       | 12          | True    | stop — window is [8,12) |
| walk       | 8           | False   | step                    |
| walk       | 9           | True    | **return 9**            |

## Complexity
- **Time:** O(√n)
- **Space:** O(1)

The jump phase takes at most √n steps and the linear walk at most √n more — about 2√n total, which is O(√n). Only a couple of index variables are kept.

## Common pitfalls
- Using a fixed jump size (like a constant 10) instead of `√n`; the √n choice is what balances the two phases and gives O(√n).
- Forgetting to **step back** by one jump before the linear scan — the first `True` is somewhere *between* the last two jump points, not at the jump point itself.
- Walking off the end during the jump or scan. Guard every access with `i < n` (the last window may be shorter than `jump`).
- Not handling the empty list (`return -1`) or the "never breaks" case (all `False` → `-1`).
- Reaching for binary search. It would find the floor, but it can require dropping a ball from the very top — a single break there leaves you stranded. The two-ball constraint is the whole point.

## Your task
Implement the function in `src/topics/search/two_crystal_balls.py`, then run:

```bash
uv run pytest -k two_crystal_balls
```

Peek at `solutions/two_crystal_balls.py` only once you've given it a real attempt.
