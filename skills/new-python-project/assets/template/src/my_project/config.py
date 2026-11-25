"""Settings for the application.

Defaults come from a JSON file inside the package. Environment variables override them.
Package data is read only through `importlib.resources`, so it works from a wheel, a zip
or an editable install. Do not build paths from `__file__`.
"""

from __future__ import annotations

import json
import os
from collections.abc import Mapping
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import Any

ENV_PREFIX = "MY_PROJECT_"
_RESOURCES = "my_project.resources"


def read_resource_text(name: str) -> str:
    """Return the text of a file in the `my_project.resources` package."""
    return files(_RESOURCES).joinpath(name).read_text(encoding="utf-8")


def load_default_config() -> dict[str, Any]:
    """Return the default configuration that ships with the package."""
    data = json.loads(read_resource_text("default_config.json"))
    if not isinstance(data, dict):
        raise ValueError("default_config.json must contain a JSON object")
    return data


@dataclass(frozen=True)
class Settings:
    """Runtime settings. Create them with `Settings.load()`."""

    output_dir: Path
    log_level: str
    greeting: str

    @classmethod
    def load(cls, environ: Mapping[str, str] | None = None) -> Settings:
        """Merge the packaged defaults with `MY_PROJECT_*` environment variables."""
        env = os.environ if environ is None else environ
        defaults = load_default_config()

        def get(key: str) -> str:
            return env.get(ENV_PREFIX + key.upper(), str(defaults[key]))

        return cls(
            output_dir=Path(get("output_dir")),
            log_level=get("log_level").upper(),
            greeting=get("greeting"),
        )
