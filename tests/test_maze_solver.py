from harness import load

m = load("maze_solver")


def _valid_path(maze, wall, start, end, path):
    if not path or path[0] != start or path[-1] != end:
        return False
    if len(set(path)) != len(path):
        return False  # no cell visited twice
    for r, c in path:
        if r < 0 or r >= len(maze) or c < 0 or c >= len(maze[r]):
            return False
        if maze[r][c] == wall:
            return False
    # each step must move to an orthogonal neighbour
    return all(
        abs(r1 - r2) + abs(c1 - c2) == 1 for (r1, c1), (r2, c2) in zip(path, path[1:], strict=False)
    )


def test_finds_a_valid_path():
    maze = [
        "....",
        ".##.",
        ".#..",
        "...#",
    ]
    start, end = (0, 0), (2, 3)
    path = m.solve(maze, "#", start, end)
    assert _valid_path(maze, "#", start, end, path)


def test_no_path_returns_empty():
    maze = [
        "..#..",
        "..#..",
        "..#..",
    ]
    path = m.solve(maze, "#", (0, 0), (0, 4))
    assert path == []


def test_start_equals_end():
    maze = ["..", ".."]
    path = m.solve(maze, "#", (0, 0), (0, 0))
    assert path == [(0, 0)]
