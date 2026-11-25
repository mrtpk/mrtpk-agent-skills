from __future__ import annotations

import pytest

from my_project.core.greeting import make_greeting


def test_make_greeting_strips_name() -> None:
    assert make_greeting("  Ada ") == "Hello, Ada!"


def test_make_greeting_custom_greeting() -> None:
    assert make_greeting("Ada", greeting="Hi") == "Hi, Ada!"


@pytest.mark.parametrize("name", ["", "   "])
def test_make_greeting_rejects_empty_name(name: str) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        make_greeting(name)
