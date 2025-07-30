"""Command‑line interface entrypoint.

This module exposes the ``oprun`` CLI when executed via ``python -m
operator_agent_orchestrator``.  It uses the `click` library to provide
subcommands.
"""

import importlib.resources as resources
import json
import os
from pathlib import Path
from typing import Optional

import click

from .orchestrator import Orchestrator
from .plugins import PLUGINS


@click.group()
def app() -> None:
    """Operator Agent Orchestrator command‑line tool.

    Use this tool to run workflows, list available plugins and copy example
    configuration files.  Run ``oprun --help`` for more information.
    """


@app.command()
@click.argument("workflow_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--log-dir", type=click.Path(file_okay=False), default=None, help="Directory where logs will be written.  Defaults to ./logs")
def run(workflow_path: str, log_dir: Optional[str]) -> None:
    """Execute a workflow defined in a YAML file.

    ``WORKFLOW_PATH`` must point to a valid YAML file describing the tasks.
    If ``--log-dir`` is provided, logs and results are written into that
    directory; otherwise a `logs/` directory is created relative to the
    current working directory.
    """
    orchestrator = Orchestrator(log_root=log_dir)
    orchestrator.run_workflow(workflow_path)


@app.command(name="list-plugins")
def list_plugins() -> None:
    """List all built‑in plugins available to workflows."""
    click.echo("Available plugins:")
    for name in sorted(PLUGINS):
        click.echo(f"- {name}")


@app.command(name="copy-example")
@click.argument("destination", type=click.Path())
def copy_example(destination: str) -> None:
    """Copy the example workflow YAML to the given DESTINATION."""
    dest = Path(destination)
    if dest.exists():
        raise click.UsageError(f"Destination {dest} already exists.")
    # Use importlib.resources to locate the example file packaged with the library
    with resources.open_binary(
        "operator_agent_orchestrator.examples", "workflow_example.yaml"
    ) as src:
        content = src.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "wb") as f:
        f.write(content)
    click.echo(f"Example workflow copied to {dest}")


if __name__ == "__main__":
    app(prog_name="oprun")