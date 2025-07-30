"""Built‑in plugin registry.

This module imports all bundled plugins and exposes them in the ``PLUGINS``
dictionary keyed by their unique names.  To add a new plugin, create a
module in this package and register it here.
"""

from .shell import ShellPlugin
from .python_function import PythonFunctionPlugin
from .csv_ingest import CSVIngestPlugin
from .metrics import MetricsPlugin


PLUGINS = {
    ShellPlugin.name: ShellPlugin,
    PythonFunctionPlugin.name: PythonFunctionPlugin,
    CSVIngestPlugin.name: CSVIngestPlugin,
    MetricsPlugin.name: MetricsPlugin,
}

__all__ = ["PLUGINS", "ShellPlugin", "PythonFunctionPlugin", "CSVIngestPlugin", "MetricsPlugin"]