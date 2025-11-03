"""Bar Tutor package initialization."""

from typing import Any

from .config import get_logger

__all__ = ["app", "get_logger"]


def __getattr__(name: str) -> Any:
    if name == "app":
        from .cli import app as cli_app

        return cli_app
    raise AttributeError(f"module 'bar_tutor' has no attribute {name!r}")
