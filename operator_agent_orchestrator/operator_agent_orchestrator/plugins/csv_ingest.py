"""CSV ingestion plugin.

This plugin reads a CSV file from disk into a pandas DataFrame and
publishes it into the shared context under the key ``dataframe``.  It
returns basic metadata about the file such as the number of rows and
columns.  Downstream tasks can then operate on the DataFrame stored in
``context['dataframe']``.
"""

from typing import Any, Dict

import pandas as pd  # type: ignore

from ..plugin_base import Plugin


class CSVIngestPlugin(Plugin):
    """Read a CSV file into a pandas DataFrame."""

    name = "csv_ingest"

    def run(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        path = config.get("path")
        if not path:
            raise ValueError("csv_ingest plugin requires a 'path' to a CSV file")
        df = pd.read_csv(path)
        # Publish to context so other tasks can access it
        context["dataframe"] = df
        return {
            "rows": len(df),
            "columns": list(df.columns),
        }