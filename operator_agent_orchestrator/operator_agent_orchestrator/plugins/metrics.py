"""Metrics computation plugin.

This plugin calculates basic statistics on numeric columns of a DataFrame
previously ingested by the ``csv_ingest`` plugin.  It expects to find
``context['dataframe']`` populated and computes mean, median and standard
deviation for the specified columns.
"""

from typing import Any, Dict, List

import pandas as pd  # type: ignore

from ..plugin_base import Plugin


class MetricsPlugin(Plugin):
    """Compute numeric metrics on a pandas DataFrame."""

    name = "metrics"

    def run(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        if "dataframe" not in context:
            raise RuntimeError("No DataFrame found in context; run csv_ingest before metrics")
        df: pd.DataFrame = context["dataframe"]
        numeric_columns: List[str] = config.get("numeric_columns", [])
        if not numeric_columns:
            # Auto‑detect numeric columns
            numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        results: Dict[str, Dict[str, float]] = {}
        for col in numeric_columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in DataFrame")
            series = df[col].dropna()
            results[col] = {
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std()),
                "min": float(series.min()),
                "max": float(series.max()),
                "count": int(series.count()),
            }
        return results