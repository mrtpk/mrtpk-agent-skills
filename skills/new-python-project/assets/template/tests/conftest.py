"""Shared fixtures. Do not change `sys.path` here: tests import the installed package."""

from __future__ import annotations

import os

import pytest

from my_project.config import ENV_PREFIX


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove `MY_PROJECT_*` variables so the host environment cannot change test results."""
    for key in list(os.environ):
        if key.startswith(ENV_PREFIX):
            monkeypatch.delenv(key)
