# Example resources for the Operator Agent Orchestrator.

"""
The ``examples`` package contains sample data and workflow definitions used
for demonstrations and tests.  You can import functions from
``plugin_example`` or copy the provided YAML and CSV files as a starting
point for your own projects.
"""

from . import plugin_example  # noqa: F401  Re-export for convenience

__all__ = ["plugin_example"]