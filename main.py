"""Entry point for the Bar Tutor Typer CLI."""

from __future__ import annotations

from bar_tutor.cli import app


def main() -> None:
    """Invoke the Typer application."""

    app()


if __name__ == "__main__":
    main()
