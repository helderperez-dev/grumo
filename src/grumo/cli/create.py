"""Deprecated alias for the canonical :command:`grumo new` scaffold."""

from __future__ import annotations

import typer

from grumo.cli.new import new

__all__ = ["create"]


def create(
    project_name: str = typer.Argument(..., help="Name of the project to create"),
) -> None:
    """Create the canonical project without installing dependencies."""
    typer.echo(
        "Warning: 'grumo create' is deprecated; use "
        "'grumo new --no-install' instead.",
        err=True,
    )
    new(project_name, template=None, variant="default", install=False)
