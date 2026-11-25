from __future__ import annotations

import pytest

from my_project import __version__
from my_project.cli import main


def test_greet_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["greet", "Ada"]) == 0
    assert capsys.readouterr().out == "Hello, Ada!\n"


def test_greet_uses_env_greeting(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("MY_PROJECT_GREETING", "Hi")
    assert main(["greet", "Ada"]) == 0
    assert capsys.readouterr().out == "Hi, Ada!\n"


def test_greet_empty_name_returns_error_code() -> None:
    assert main(["greet", " "]) == 2


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_missing_command_exits_with_usage_error() -> None:
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2
