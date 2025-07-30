"""Core workflow execution engine.

The :class:`Orchestrator` class loads a workflow definition from a YAML file,
resolves task dependencies, executes tasks concurrently using asyncio and
records structured logs.  Tasks are defined by plugins listed in
``operator_agent_orchestrator.plugins`` and specified in the workflow file.
"""

from __future__ import annotations

import asyncio
import datetime
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .plugins import PLUGINS


class Orchestrator:
    """Load and execute workflows composed of dependent tasks.

    Parameters
    ----------
    log_root:
        Optional root directory where run logs should be written.  If None,
        a `logs/` directory will be created relative to the current working
        directory.
    """

    def __init__(self, log_root: Optional[str] = None) -> None:
        self.log_root = Path(log_root) if log_root else Path("logs")
        self.log_root.mkdir(parents=True, exist_ok=True)

    def run_workflow(self, workflow_path: str) -> None:
        """Synchronously run a workflow definition.

        Internally, this method invokes :func:`asyncio.run` on the
        asynchronous implementation.  Results and logs are written to disk
        when execution completes.

        Parameters
        ----------
        workflow_path:
            Path to a YAML file describing the workflow.
        """
        asyncio.run(self._run_workflow_async(workflow_path))

    async def _run_workflow_async(self, workflow_path: str) -> None:
        # Load the YAML
        with open(workflow_path, "r", encoding="utf-8") as f:
            definition = yaml.safe_load(f)
        tasks_def = definition.get("tasks") or []
        name = definition.get("name", "unnamed-workflow")
        description = definition.get("description", "")

        # Create run directory
        ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        run_dir = self.log_root / f"{Path(workflow_path).stem}_{ts}"
        run_dir.mkdir(parents=True, exist_ok=True)

        # Set up logger
        logger = logging.getLogger(f"orchestrator.{ts}")
        logger.setLevel(logging.INFO)
        # File handler
        fh = logging.FileHandler(run_dir / "run.log", encoding="utf-8")
        fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(fh)
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(ch)

        logger.info(f"Starting workflow: {name}")
        if description:
            logger.info(description)

        # Validate tasks and build data structures
        tasks: Dict[str, Dict[str, Any]] = {}
        for idx, t in enumerate(tasks_def):
            tid = t.get("id")
            if not tid or not isinstance(tid, str):
                raise ValueError(f"Task at index {idx} is missing a string 'id'")
            if tid in tasks:
                raise ValueError(f"Duplicate task id '{tid}'")
            plugin_name = t.get("plugin")
            if plugin_name not in PLUGINS:
                raise ValueError(f"Unknown plugin '{plugin_name}' for task '{tid}'")
            config = t.get("config", {})
            depends_on = t.get("depends_on", []) or []
            if not isinstance(depends_on, list):
                raise ValueError(f"'depends_on' for task '{tid}' must be a list")
            tasks[tid] = {
                "plugin": plugin_name,
                "config": config,
                "depends_on": depends_on,
            }

        # Shared context for tasks to publish results
        context: Dict[str, Any] = {}
        results: Dict[str, Any] = {}

        # Keep futures for tasks
        task_futures: Dict[str, asyncio.Future] = {}

        async def run_single_task(task_id: str) -> Any:
            # Wait for dependencies
            for dep in tasks[task_id]["depends_on"]:
                fut = task_futures.get(dep)
                if fut:
                    await fut
            plugin_name = tasks[task_id]["plugin"]
            config = tasks[task_id]["config"]
            plugin_cls = PLUGINS[plugin_name]
            plugin = plugin_cls()
            logger.info(f"Running task {task_id} using plugin {plugin_name}...")
            try:
                result = await asyncio.to_thread(plugin.run, config, context)
                logger.info(f"Task {task_id} completed")
            except Exception as exc:  # noqa: BLE001
                logger.exception(f"Task {task_id} failed: {exc}")
                result = {"error": str(exc)}
            # Save result
            context[task_id] = result
            results[task_id] = result
            return result

        # Schedule all tasks at once; run_single_task awaits dependencies
        for tid in tasks:
            task_futures[tid] = asyncio.create_task(run_single_task(tid))

        # Wait for all tasks to finish
        await asyncio.gather(*task_futures.values())

        # Persist results
        summary_path = run_dir / "summary.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Workflow finished. Results written to {summary_path}")
