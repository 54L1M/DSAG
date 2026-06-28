"""Test harness: load the implementation currently under practice.

Tests never import your code by a fixed path. Instead they call ``load(name)``,
which finds ``<name>.py`` inside the *active target* directory and imports it.
That lets the exact same test suite run against:

  * ``src/topics/`` (the nested study workspace)   -> default
  * ``src/days/dayN/`` (a flat drill copy)          -> after ``python drill.py``
  * ``solutions/`` (the worked reference impls)     -> ALGO_TARGET=solutions

Resolution order for the active target:
  1. the ``ALGO_TARGET`` environment variable, if set
  2. the first line of the ``.algo-target`` file
  3. fallback to ``src/topics``
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent
DEFAULT_TARGET = "src/topics"


def target_root() -> Path:
    """Return the directory holding the implementations currently under test."""
    target = os.environ.get("ALGO_TARGET")
    if not target:
        cfg = ROOT / ".algo-target"
        if cfg.exists():
            target = cfg.read_text().strip()
    if not target:
        target = DEFAULT_TARGET
    root = (ROOT / target).resolve()
    if not root.exists():
        raise FileNotFoundError(
            f"Active target '{target}' does not exist (resolved to {root}). "
            "Check .algo-target or the ALGO_TARGET env var."
        )
    return root


def load(name: str) -> ModuleType:
    """Find ``<name>.py`` under the active target and import it as a module.

    Searches recursively, so it works for both the nested ``src/topics`` layout
    and the flat ``src/days/dayN`` layout.
    """
    root = target_root()
    matches = sorted(root.rglob(f"{name}.py"))
    if not matches:
        raise ImportError(
            f"Could not find '{name}.py' under {root}. "
            "Did you run drill.py, or is the file named differently?"
        )
    if len({m.name for m in matches}) > 1 or len(matches) > 1:
        # Multiple files with the same name would be ambiguous; the layouts here
        # guarantee uniqueness, so this is just a guard against accidental copies.
        matches = matches[:1]
    path = matches[0]

    # Import under a unique, target-scoped name so re-runs against a different
    # target don't return a stale cached module.
    mod_name = f"_algo_{root.name}_{name}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError(f"Could not build import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module
    spec.loader.exec_module(module)
    return module
