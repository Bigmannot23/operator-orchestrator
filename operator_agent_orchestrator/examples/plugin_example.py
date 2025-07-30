"""Example functions for use with the python_function plugin.

This module contains small functions that can be invoked by the
``python_function`` plugin.  You can import functions from here or
create your own module with whatever logic you need.  Functions must
return JSON‑serialisable values.
"""

from typing import Any, Dict, List


def greet(name: str) -> str:
    """Return a friendly greeting for the given name."""
    return f"Hello, {name}!"


def sum_numbers(numbers: List[float]) -> float:
    """Return the sum of a list of numbers."""
    return float(sum(numbers))


def flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten a nested dictionary into a single level using dot‑separated keys.

    Parameters
    ----------
    d:
        The dictionary to flatten.
    parent_key:
        The prefix to prepend to keys in ``d`` (used during recursion).
    sep:
        Separator to use between nested key parts.

    Returns
    -------
    Dict[str, Any]
        A new dictionary with flattened keys.
    """
    items: List[tuple[str, Any]] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)