"""Unit tests for the Operator Agent Orchestrator."""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from operator_agent_orchestrator import Orchestrator

import importlib.resources as resources


class OrchestratorTest(unittest.TestCase):
    """Test the end‑to‑end execution of a simple workflow."""

    def test_run_example_workflow(self) -> None:
        # Copy the example workflow and sample data into a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            # Write workflow file
            workflow_bytes = resources.files(
                "operator_agent_orchestrator.examples"
            ).joinpath("workflow_example.yaml").read_bytes()
            workflow_path = tmpdir_path / "workflow.yaml"
            workflow_path.write_bytes(workflow_bytes)
            # Write sample CSV
            csv_bytes = resources.files(
                "operator_agent_orchestrator.examples"
            ).joinpath("sample_data.csv").read_bytes()
            sample_csv_path = tmpdir_path / "sample_data.csv"
            sample_csv_path.write_bytes(csv_bytes)

            # Update workflow file to reference the temp CSV path
            workflow_text = workflow_path.read_text()
            replaced = workflow_text.replace(
                "operator_agent_orchestrator/examples/sample_data.csv",
                str(sample_csv_path)
            )
            workflow_path.write_text(replaced)

            # Run orchestrator
            orchestrator = Orchestrator(log_root=str(tmpdir_path / "logs"))
            orchestrator.run_workflow(str(workflow_path))

            # Ensure logs directory is created
            logs_dir = tmpdir_path / "logs"
            self.assertTrue(logs_dir.exists())
            # Find summary.json
            summaries = list(logs_dir.rglob("summary.json"))
            self.assertEqual(len(summaries), 1)
            summary_path = summaries[0]
            with open(summary_path, "r", encoding="utf-8") as f:
                summary = json.load(f)
            # Basic assertions about results
            self.assertIn("ingest", summary)
            self.assertEqual(summary["ingest"]["rows"], 5)
            self.assertIn("metrics", summary)
            self.assertIn("age", summary["metrics"])
            self.assertEqual(summary["metrics"]["age"]["count"], 5)
            self.assertIn("greet", summary)
            self.assertEqual(summary["greet"], "Hello, Operator!")
            self.assertIn("announce", summary)
            self.assertEqual(summary["announce"]["returncode"], 0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()