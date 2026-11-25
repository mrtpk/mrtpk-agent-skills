"""Run the package as a separate process, the same way a user runs it."""

from __future__ import annotations

import subprocess
import sys

import pytest

pytestmark = pytest.mark.integration


def run_module(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "my_project", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_module_runs_greet() -> None:
    result = run_module("greet", "Ada")
    assert result.returncode == 0, result.stderr
    assert result.stdout == "Hello, Ada!\n"


def test_module_reports_bad_input() -> None:
    result = run_module("greet", "")
    assert result.returncode == 2
    assert "must not be empty" in result.stderr
