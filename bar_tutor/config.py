"""Logging utilities for the Bar Tutor project."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

_DEFAULT_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
_ROOT_LOGGER_NAME = "bar_tutor"


def _resolve_log_path(log_path: Optional[Path]) -> Path:
    """Return the absolute log path, defaulting to the project root."""

    if log_path is not None:
        return Path(log_path).expanduser().resolve()

    project_root = Path(__file__).resolve().parents[1]
    return project_root / "bar_tutor.log"


def get_logger(
    name: str = _ROOT_LOGGER_NAME,
    *,
    log_path: Optional[Path] = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """Return a configured logger with safe file-handler fallback.

    The first call configures a shared root logger. Subsequent calls simply
    retrieve child loggers without reconfiguring handlers.
    """

    root_logger = logging.getLogger(_ROOT_LOGGER_NAME)
    if not root_logger.handlers:
        handlers: list[logging.Handler] = []

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
        handlers.append(stream_handler)

        target_path = _resolve_log_path(log_path)
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(target_path, encoding="utf-8")
        except (OSError, PermissionError) as exc:
            stream_handler.stream.write(
                f"[bar-tutor] File logging disabled, continuing with console-only logging: {exc}\n"
            )
        else:
            file_handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
            handlers.append(file_handler)

        logging.basicConfig(level=level, handlers=handlers, force=True)

    return logging.getLogger(name)


__all__ = ["get_logger"]
