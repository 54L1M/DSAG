# Linear Search

> search · stub: `src/topics/search/linear_search.py` · test: `tests/test_linear_search.py`
>
> 📚 Need more detail? See the [in-depth version](linear_search.deep.md).

## Intuition
Look at each item one by one, from the front, until you spot the one you want. It's exactly how you'd find a friend's name on an unsorted guest list: start at the top and read down until you hit it. No cleverness, no assumptions about order — just a steady scan.

## How it works
1. Start at index `0`.
2. Compare the current element to `target`.
3. If it matches, return that index immediately (first match wins).
4. Otherwise move to the next index and repeat.
5. If you fall off the end without a match, return `-1`.

Worked example — search for `7` in `[9, 1, 7, 3]`:

| step | index | value | value == 7? | action          |
|------|-------|-------|-------------|-----------------|
| 1    | 0     | 9     | no          | move on         |
| 2    | 1     | 1     | no          | move on         |
| 3    | 2     | 7     | yes         | **return 2**    |

Searching for something absent (`99` in `[1, 2, 3]`) walks all three slots, finds nothing, and returns `-1`.

## Complexity
- **Time:** O(n)
- **Space:** O(1)

In the worst case (target is last or missing) you touch every one of the `n` elements, and you only ever keep a single index variable.

## Common pitfalls
- Returning `True`/`False` instead of the **index** (or `-1`). The contract is a position.
- Returning the wrong sentinel — it must be `-1`, not `None` or `0`.
- Forgetting the empty-list case; a clean loop handles it naturally by returning `-1`.
- Returning the *last* match instead of the *first* — stop as soon as you find one.
- Assuming the list is sorted. Linear search must work on unsorted data, so don't add early-exit "it's bigger so stop" logic.

## Your task
Implement the function in `src/topics/search/linear_search.py`, then run:

```bash
uv run pytest -k linear_search
```

Peek at `solutions/linear_search.py` only once you've given it a real attempt.
