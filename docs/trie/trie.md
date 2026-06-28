# Trie (Prefix Tree)

> trie · stub: `src/topics/trie/trie.py` · test: `tests/test_trie.py`
>
> 📚 Need more detail? See the [in-depth version](trie.deep.md).

## Intuition

A trie stores words by their *shared prefixes* instead of as separate strings.
Words that begin the same way share the same starting path through the tree, so
"car", "card", and "cat" all reuse the `c -> a` branch. This makes
prefix questions ("which words start with `ca`?") fast — exactly what powers
autocomplete. Think of an index-tabbed dictionary: flip to `c`, then `a`, and
everything under that tab shares the prefix.

## How it works

Each **node** holds two things:

- `children`: a dict mapping a single `char` -> child node.
- `is_word`: a boolean flag, `True` if a word *ends* at this node.

The tree starts at an empty `root`. Inserting `cat`, `car`, `card`, `dog`:

```
        (root)
        /     \
       c       d
       |       |
       a       o
      / \      |
     r   t*    g*
     |
     d*          ( * = is_word True )
```

Notice `car` ends at the `r` node (`is_word=True`) **and** that same `r` node has
a child `d` leading to `card`. A node can be both a complete word and a prefix.

**insert(word)** — start at `root`; for each char, follow the child or create it
(`setdefault`). After the last char, set `is_word = True`. O(len(word)).

**contains(word)** — walk char by char from `root`. If any char is missing,
return `False`. After reaching the end, return that node's `is_word`. This is why
`contains("ca")` is `False` even though `cat`/`car` exist — the `a` node has
`is_word=False`. It's a *prefix*, not a stored word.

**starts_with(prefix)** — walk to the prefix node (return `[]` if the path
breaks). Then **DFS** down from that node, accumulating the string as you go; at
every node with `is_word=True`, record the accumulated word. Finally **sort** the
results. For prefix `ca`:

```
walk c -> a, then DFS:
  a (not word) -> r (word: "car") -> d (word: "card")
               -> t (word: "cat")
collected: ["car","card","cat"]  (already / after sort)
```

**delete(word)** — walk to the word's end node; if found, set `is_word = False`.
The structure stays (children of deeper words are untouched), the word just stops
counting as stored. Deleting a missing word is a harmless no-op. Pruning empty
nodes is optional.

## Complexity

- **Time:** insert / contains / delete are O(L) where L = word length;
  `starts_with` is O(P + K) to find the prefix and collect K result chars, plus
  the sort.
- **Space:** O(total characters across all inserted words).

Each operation only touches nodes along the word's path (plus the subtree for
`starts_with`), never the whole word set.

## Common pitfalls

- **Prefix vs full word.** A node existing does not mean a word ends there —
  always gate `contains` on `is_word`, not just "the path exists".
- **Forgetting to sort `starts_with`.** Dict iteration order isn't lexicographic;
  the tests expect `["car","card","cat"]`, so sort before returning.
- **Delete by *unsetting the flag*.** Don't rip out shared nodes — deleting `cat`
  must leave `car` intact. Just set `is_word = False`.
- **Missing prefix node.** If the prefix path breaks (e.g. `starts_with("z")`),
  return `[]` rather than crashing on a `None` lookup.
- **Empty string / re-insert.** Inserting the same word twice is fine (idempotent
  flag); make sure that doesn't duplicate it in `starts_with` output.

## Your task

Implement in `src/topics/trie/trie.py`, then run:

```bash
uv run pytest -k trie
```

Peek at `solutions/trie.py` only once you've given it a real attempt.
