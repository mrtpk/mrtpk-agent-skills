"""my-project: short description of the package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("my-project")
except PackageNotFoundError:  # pragma: no cover - package is not installed
    __version__ = "0.0.0"

__all__ = ["__version__"]
