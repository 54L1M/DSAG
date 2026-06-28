"""Maze solver — recursive backtracking from start to end."""

from __future__ import annotations

from common.types import Point


def solve(maze: list[str], wall: str, start: Point, end: Point) -> list[Point]:
    """Return a path of points from `start` to `end`, inclusive.

    `maze` is a list of equal-length strings (rows). A cell equal to `wall` is
    impassable; any other character is walkable. Points are (row, col).

    Use recursive backtracking: from the current cell, try the four neighbours
    (up/down/left/right). Base cases that make a step invalid: off the grid, on
    a wall, or already visited. When you reach `end`, record it and unwind,
    appending each cell to the path on the way back.

    Return the path from start to end (order either way is fine as long as it is
    a contiguous walk). If there is no path, return an empty list.

    Time: O(rows * cols). Space: O(rows * cols).
    """
    raise NotImplementedError  # remove this line and implement
