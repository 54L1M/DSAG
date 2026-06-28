# Trie (Prefix Tree) — In Depth

> In-depth companion · trie · stub: `src/topics/trie/trie.py` · test: `tests/test_trie.py`
>
> New here? Read the [quick version](trie.md) first.

## The mental model

A hash set of strings stores each word as an opaque blob — it can answer "is
*exactly* this word here?" in O(1), but it has no idea that `card` and `car`
share four letters. A trie throws away the "store whole strings" idea and instead
stores **letters on edges of a tree**, so that any words sharing a prefix share
the same path from the root.

The single mental picture to hold:

> A word is *spelled out* by walking from the root, one character per step. The
> word "is in the trie" if and only if that walk lands on a node whose
> `is_word` flag is `True`.

Two consequences fall straight out of that picture and explain almost every test:

- Reaching a node by spelling a string does **not** mean the string is a stored
  word. The node might just be a waypoint on the way to longer words. That's why
  `contains("ca")` is `False` — you can walk `c -> a`, but the `a` node has
  `is_word=False`.
- Everything below a node shares the prefix you spelled to get there. So
  "find all words starting with `ca`" is just "walk to the `a` node, then collect
  every flagged node beneath it."

Each node is two things: `children`, a dict mapping one `char -> child node`, and
`is_word`, a boolean. (The reference uses a tiny `_TrieNode` class with
`__slots__`, but `{char: child}` plus a flag is the whole idea.)

## Why it works — the invariant

> **Invariant:** for any string `s`, `s` is a stored word **iff** following `s`'s
> characters from the root succeeds at every step *and* the final node has
> `is_word == True`.

Each method is just a faithful reading of that one sentence:

- `insert(s)` makes the walk for `s` succeed (creating nodes as needed) and then
  sets the final flag — i.e. it makes the invariant evaluate `True` for `s`.
- `contains(s)` evaluates the invariant directly: walk, then check the flag.
- `delete(s)` makes the invariant evaluate `False` for `s` by clearing the flag,
  while leaving the *walk* intact so other words that pass through aren't harmed.
- `starts_with(p)` walks to `p`'s node, then enumerates every `s` for which the
  invariant holds in that subtree.

Because the flag is *separate* from node existence, a node can simultaneously be
a complete word and a prefix of longer words (e.g. `car` and `card`). That
separation is the whole reason the structure handles overlapping words cleanly.

## The tree for cat / car / card / dog

Inserting `cat`, `car`, `card`, `dog` (`*` marks `is_word == True`):

```
                (root)
               /      \
             c          d
             |          |
             a          o
            / \         |
           r*  t*       g*
           |
           d*
```

Read off the invariant on this tree:

- `contains("car")` → walk `c,a,r`, node `r` has `*` → `True`.
- `contains("ca")`  → walk `c,a`, node `a` has no `*` → `False` (a prefix).
- `contains("cats")`→ walk `c,a,t`, then no `s` child → walk fails → `False`.
- `r` is both a word (`car*`) and a prefix (it has child `d` for `card`). A single
  node wears both hats at once.

## Detailed walkthrough

```python
def insert(self, word):
    node = self.root
    for ch in word:
        node = node.children.setdefault(ch, _TrieNode())
    node.is_word = True
```

`setdefault(ch, _TrieNode())` is the heart: "give me the child for `ch`; if it
doesn't exist, create an empty node, store it, and return it." So the loop walks
down, *extending the tree only where it must*. After consuming every character,
the final node is flagged. Inserting the same word twice just re-sets an already
`True` flag — idempotent, no duplicates created.

```python
def _find_node(self, s):
    node = self.root
    for ch in s:
        nxt = node.children.get(ch)
        if nxt is None:
            return None          # walk broke -> s isn't even a prefix
        node = nxt
    return node                  # node reached by spelling s (flag unchecked)
```

`_find_node` is the shared "walk" primitive. Crucially it returns the node
*without* consulting `is_word` — both `contains` and `starts_with` build on it but
interpret the result differently.

```python
def contains(self, word):
    node = self._find_node(word)
    return node is not None and node.is_word     # walk AND flag
```

This is the invariant verbatim: the walk must succeed *and* the flag must be set.
Dropping the `and node.is_word` is the classic bug that makes prefixes report as
words.

```python
def starts_with(self, prefix):
    node = self._find_node(prefix)
    if node is None:
        return []                                # prefix path broke
    out = []
    self._collect(node, prefix, out)
    out.sort()                                   # tests require sorted output
    return out

def _collect(self, node, prefix, out):
    if node.is_word:
        out.append(prefix)
    for ch, child in node.children.items():
        self._collect(child, prefix + ch, out)
```

`contains` vs `starts_with` is the key contrast: `contains` reads one flag at the
end of the walk; `starts_with` *DFS-collects* every flagged node in the subtree,
rebuilding each word by accumulating `prefix + ch` as it descends. Dict iteration
order is not lexicographic, so the explicit `out.sort()` is what makes the result
deterministic — exactly what `test_starts_with_autocomplete` asserts
(`["car", "card", "cat"]`).

```python
def delete(self, word):
    node = self._find_node(word)
    if node is not None:
        node.is_word = False
```

Delete only flips the flag off. The nodes — and therefore every longer word that
passes through them — stay intact. Deleting a missing word finds no node (or a
node whose flag is already `False`) and changes nothing: a clean no-op, as
`test_delete` requires.

## Complexity, derived

Let `L` be the length of the word/prefix, and let `N` be the number of words
stored.

- **insert / contains / delete: O(L).** Each walks `L` characters; every step is
  one dict lookup or `setdefault`, which is O(1) average. The work depends only on
  the *length of this word*, **not on `N`**. This is the headline property:
  adding millions of other words doesn't slow down a lookup of `"cat"`.
- **starts_with: O(L + S + K log K).** O(L) to walk to the prefix node, O(S) to
  DFS the subtree of total size `S` (number of characters in the collected
  results), and O(K log K) to sort the `K` matched words. The dominant term is
  whatever the result set requires — it can't be cheaper than reading out the
  answers.

**Contrast with a hash set.** A `set[str]` gives O(L) membership too (you still
hash all `L` characters), and uses less constant overhead per word. But ask it
"which words start with `ca`?" and it has no structure to exploit — it must scan
**all N words** and filter, O(N · L). The trie answers the same query in time
proportional to the *matches*, independent of `N`. Prefix queries are precisely
where the trie earns its keep.

**Space.** O(total characters across all inserted words) in the worst case (no
sharing), but shared prefixes are stored once, so dictionary-like word sets
compress well. Each node also carries fixed overhead: a `dict` plus a bool.

## Edge cases in detail

- **`contains("ca")` is `False`** (from `test_insert_and_contains`). The walk
  succeeds but `is_word` is `False` — a prefix is not a word. This is the single
  most important behaviour to internalize.
- **`contains("cats")` is `False`.** The walk breaks at the missing `s` child;
  `_find_node` returns `None`.
- **`starts_with` must be sorted.** Insertion/dict order would give a nondeterministic
  order; the test pins the exact sorted list.
- **`starts_with("z")` is `[]`.** No `z` child off the root → `_find_node` returns
  `None` → early `[]` (no crash on a `None`).
- **Delete missing is a no-op** (`test_delete` deletes `"nope"`). No node found,
  nothing changes; `starts_with("ca")` is unaffected.
- **A word that is also a prefix of another** (`car` / `card`, from
  `test_prefix_is_word_too`). The `r` node is flagged *and* has a `d` child;
  `contains("car")` is `True` and `starts_with("car")` returns both `["car",
  "card"]`. Deleting `car` would clear only `r`'s flag and leave `card` reachable.
- **Re-inserting a word** is idempotent — it never appears twice in
  `starts_with`, because "word-ness" is a single boolean, not a count.

## Variations & trade-offs

- **Compressed / radix trie (PATRICIA).** Long non-branching chains (like the
  `c -> a -> r -> d` spine) waste a node per character. A radix trie stores a
  whole substring on an edge and only splits where words diverge, cutting node
  count and pointer-chasing at the cost of more complex insert/split logic.
- **Autocomplete ranking.** `starts_with` here returns *all* matches sorted
  lexicographically. Real autocomplete usually wants the *top-k by frequency or
  recency*. Store a count/weight on word nodes and collect into a heap, or cache
  the best completions at each node, instead of sorting alphabetically.
- **Character-set assumptions.** A `dict` of children handles any character
  (Unicode, digits, punctuation) and stays sparse. If the alphabet is small and
  fixed (e.g. lowercase a–z), a 26-slot array per node trades memory for slightly
  faster, allocation-free child access. The reference uses a dict — flexible and
  simple.
- **Pruning on delete.** The reference leaves dead nodes after a delete. An
  optional improvement: after clearing the flag, walk back up and remove any node
  that now has no children and isn't a word, reclaiming space. It complicates
  delete (you need the path back to the root) and isn't required by the tests.

## Connections

- **`../hashing/map.md`** — each node's `children` is a dict (hash map) from char
  to child. The trie is, in a sense, a tree *of* hash maps: O(1) child access at
  every level is what gives each step its O(1) cost.
- **`../trees/bt_pre_order.md`** — `starts_with`'s `_collect` is a pre-order DFS
  over a tree: visit the node (record it if `is_word`), then recurse into each
  child. If you understand tree pre-order traversal, you already understand how
  the trie enumerates words.

## Self-check

1. Why is `contains("ca")` `False` after inserting `cat` and `car`, even though
   the walk `c -> a` succeeds? State it in terms of the invariant.
2. What single line in `contains` prevents prefixes from being reported as words,
   and what breaks if you drop it?
3. Why does `starts_with` need an explicit `sort()` — what determines the natural
   order of `_collect`'s output, and why isn't it lexicographic?
4. After `insert("car"); insert("card"); delete("car")`, what does
   `contains("card")` return, and why didn't deleting `car` remove the `c-a-r`
   path?
5. For prefix queries, give the big-O of a trie versus a hash set, and explain
   the difference in one sentence.
6. If every node shared one mutable default `children` dict, what would
   `insert("cat")` then `insert("dog")` produce? Why is a fresh dict per node
   essential?

## Deep dive: common bugs

- **Treating any reached node as a word (ignoring `is_word`).** Writing
  `return self._find_node(word) is not None` makes `contains("ca")` wrongly return
  `True`. The fix is the invariant: the walk must succeed **and** the final node's
  `is_word` must be `True`. Node existence proves *prefix*, not *word*.
- **Forgetting to sort `starts_with`.** Returning `_collect`'s output as-is yields
  whatever order the child dicts happen to iterate in — often insertion order, not
  alphabetical. `test_starts_with_autocomplete` expects exactly
  `["car", "card", "cat"]`, so the missing `out.sort()` fails the test even though
  every right word is present.
- **Sharing a mutable default among nodes.** A subtle Python trap: if children
  were created via a shared object (e.g. a mutable default argument, or assigning
  the *same* dict instance to every node), inserting into one node would mutate
  *all* nodes. Then `insert("cat")` and `insert("dog")` would tangle their
  branches together. Each node must get its **own** fresh `children` dict —
  which is exactly what `_TrieNode.__init__` (or `setdefault(ch, _TrieNode())`)
  guarantees.
- **Deleting by removing nodes instead of clearing the flag.** Ripping out the
  `c-a-r` path to delete `car` would also destroy `card`. Delete must only set
  `is_word = False` (pruning, if done, must stop at any node that is still a word
  or still has children).
