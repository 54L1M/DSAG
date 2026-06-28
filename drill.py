"""Drill / reset helper.

Repetition builds muscle memory. When you want to re-solve everything from a
blank slate, run::

    uv run python drill.py

It copies the pristine stubs from ``stubs/`` into a fresh ``src/days/dayN/``
folder and points the test target at it. Run it again tomorrow for ``day2``,
and so on. Your earlier study work in ``src/topics/`` is left untouched.

To go back to the nested study workspace::

    uv run python drill.py --topics
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STUBS = ROOT / "stubs"
DAYS = ROOT / "src" / "days"
TARGET_FILE = ROOT / ".algo-target"


def _set_target(rel: str) -> None:
    TARGET_FILE.write_text(rel + "\n")
    print(f"Active target -> {rel}")


def _next_day() -> Path:
    DAYS.mkdir(parents=True, exist_ok=True)
    existing = [
        int(p.name[3:])
        for p in DAYS.iterdir()
        if p.is_dir() and p.name.startswith("day") and p.name[3:].isdigit()
    ]
    n = (max(existing) + 1) if existing else 1
    return DAYS / f"day{n}"


def new_day() -> None:
    if not STUBS.exists():
        raise SystemExit("stubs/ not found — nothing to copy.")
    day = _next_day()
    day.mkdir(parents=True)
    count = 0
    for stub in sorted(STUBS.glob("*.py")):
        shutil.copy2(stub, day / stub.name)
        count += 1
    rel = day.relative_to(ROOT).as_posix()
    print(f"Created {rel} with {count} fresh stubs.")
    _set_target(rel)
    print("\nGo drill! Run:  uv run pytest")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--topics",
        action="store_true",
        help="point the test target back at src/topics (the study workspace)",
    )
    group.add_argument(
        "--show",
        action="store_true",
        help="print the current active target and exit",
    )
    args = parser.parse_args()

    if args.show:
        current = TARGET_FILE.read_text().strip() if TARGET_FILE.exists() else "src/topics"
        print(current)
        return
    if args.topics:
        _set_target("src/topics")
        return
    new_day()


if __name__ == "__main__":
    main()
