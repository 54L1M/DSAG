# Big-O — the one mental model behind everything

Big-O describes **how the work an algorithm does grows as the input grows**. It
ignores constants and small terms and asks only: when `n` doubles, what happens?

You'll annotate every exercise here with its time and space complexity. Get
comfortable eyeballing it.

## The common classes (best to worst)

| Notation | Name | "When n doubles, work…" | Example |
|---|---|---|---|
| O(1) | constant | …stays the same | array index, hash lookup, stack push |
| O(log n) | logarithmic | …grows by one step | binary search, heap insert |
| O(n) | linear | …doubles | linear search, one pass over a list |
| O(n log n) | linearithmic | …slightly more than doubles | merge sort, quick sort (avg), good comparison sorts |
| O(n²) | quadratic | …quadruples | bubble/insertion sort, nested loops over the same data |
| O(2ⁿ) | exponential | …squares | naive recursive subsets, brute-force combinatorics |

## How to read code for Big-O

- **A single loop over n items** → O(n).
- **A loop inside a loop, both over n** → O(n²).
- **Halving the problem each step** (binary search, balanced-tree descent) →
  O(log n).
- **Divide in half AND touch every element to recombine** (merge sort) →
  O(n log n).
- **Recursion**: (number of calls) × (work per call). Drawing the recursion
  tree helps.

## Rules of thumb

- **Drop constants:** O(2n) and O(n/2) are both just O(n).
- **Keep the dominant term:** O(n² + n) is O(n²).
- **Worst case by default.** Quick sort is O(n log n) *average* but O(n²)
  *worst*; say which you mean.
- **Time vs space are separate.** Merge sort is O(n log n) time but O(n) extra
  space; an in-place sort might be O(1) space.
- **Amortized** ≠ per-call. A dynamic array's `push` is O(n) on the rare resize
  but O(1) *amortized* across many pushes.

## Why it matters here

Most of these exercises have an obvious slow solution and a clever fast one. The
*point* of practicing is to feel the difference — e.g. searching a sorted list
linearly (O(n)) vs. binary search (O(log n)), or finding the breaking floor with
two crystal balls in O(√n) instead of O(n). When you finish an exercise, always ask:
"what's the complexity, and could it be better?"
