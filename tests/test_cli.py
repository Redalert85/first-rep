"""Basic smoke tests for the Bar Tutor CLI."""

from __future__ import annotations

from typer.testing import CliRunner

from bar_tutor.cli import app


runner = CliRunner()


def test_help_displays_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Utilities for inspecting the Bar Tutor knowledge base" in result.stdout


def test_summary_outputs_totals() -> None:
    result = runner.invoke(app, ["summary"])
    assert result.exit_code == 0
    assert "Total concepts" in result.stdout
