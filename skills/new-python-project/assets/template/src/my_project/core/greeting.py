"""Example domain module. Replace it with your own logic."""

from __future__ import annotations


def make_greeting(name: str, greeting: str = "Hello") -> str:
    """Return a greeting for `name`."""
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must not be empty")
    return f"{greeting}, {cleaned}!"
