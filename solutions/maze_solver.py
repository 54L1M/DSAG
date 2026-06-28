"""Reference solution — maze solver (recursive backtracking)."""

from __future__ import annotations

from common.types import Point

_DIRECTIONS: list[Point] = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def solve(maze: list[str], wall: str, start: Point, end: Point) -> list[Point]:
    if not maze:
        return []
    seen = [[False] * len(row) for row in maze]
    path: list[Point] = []
    if _walk(maze, wall, start, end, seen, path):
        return path
    return []


def _walk(
    maze: list[str],
    wall: str,
    curr: Point,
    end: Point,
    seen: list[list[bool]],
    path: list[Point],
) -> bool:
    r, c = curr
    # Off the grid.
    if r < 0 or r >= len(maze) or c < 0 or c >= len(maze[r]):
        return False
    # Wall or already visited.
    if maze[r][c] == wall or seen[r][c]:
        return False

    seen[r][c] = True
    path.append(curr)

    if curr == end:
        return True

    for dr, dc in _DIRECTIONS:
        if _walk(maze, wall, (r + dr, c + dc), end, seen, path):
            return True

    path.pop()
    return False
