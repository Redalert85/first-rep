"""Command line interface for the Bar Tutor project."""

from __future__ import annotations

from collections import Counter
from typing import Optional

import typer

from .config import get_logger
from bar_tutor_unified import LegalKnowledgeGraph

app = typer.Typer(help="Utilities for inspecting the Bar Tutor knowledge base")
logger = get_logger(__name__)


def _load_graph() -> LegalKnowledgeGraph:
    """Create a knowledge graph instance with logging."""

    logger.debug("Loading legal knowledge graph")
    return LegalKnowledgeGraph()


def _subject_counts(graph: LegalKnowledgeGraph) -> Counter[str]:
    return Counter(node.subject for node in graph.nodes.values())


@app.command()
def subjects() -> None:
    """List all subjects tracked by the knowledge graph."""

    graph = _load_graph()
    counts = _subject_counts(graph)
    typer.echo("Subjects:")
    for subject in sorted(counts):
        typer.echo(f"  - {subject.replace('_', ' ').title()} ({counts[subject]} concepts)")


@app.command()
def concepts(subject: Optional[str] = typer.Option(None, help="Filter by subject")) -> None:
    """Display concepts, optionally filtered by subject."""

    graph = _load_graph()
    nodes = graph.nodes.values()
    if subject:
        normalized = subject.lower().replace(" ", "_")
        nodes = [node for node in nodes if node.subject == normalized]
        if not nodes:
            typer.echo(f"No concepts found for subject '{subject}'.")
            raise typer.Exit(code=1)

    for node in nodes:
        typer.echo(f"- {node.name} [{node.subject}] (difficulty: {node.difficulty})")


@app.command()
def summary() -> None:
    """Show a high-level summary of the knowledge graph."""

    graph = _load_graph()
    counts = _subject_counts(graph)
    total = sum(counts.values())
    typer.echo(f"Total concepts: {total}")
    typer.echo("Subject breakdown:")
    for subject, count in counts.most_common():
        typer.echo(f"  • {subject.replace('_', ' ').title()}: {count}")


__all__ = ["app"]


if __name__ == "__main__":
    app()
