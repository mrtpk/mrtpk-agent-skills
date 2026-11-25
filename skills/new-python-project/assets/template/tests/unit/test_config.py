from __future__ import annotations

from pathlib import Path

from my_project.config import Settings, load_default_config


def test_default_config_ships_with_package() -> None:
    assert load_default_config()["greeting"] == "Hello"


def test_settings_use_defaults() -> None:
    settings = Settings.load(environ={})
    assert settings.output_dir == Path("output")
    assert settings.log_level == "INFO"


def test_settings_env_overrides_defaults(tmp_path: Path) -> None:
    env = {"MY_PROJECT_OUTPUT_DIR": str(tmp_path), "MY_PROJECT_LOG_LEVEL": "debug"}
    settings = Settings.load(environ=env)
    assert settings.output_dir == tmp_path
    assert settings.log_level == "DEBUG"
