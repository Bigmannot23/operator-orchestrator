"""Base classes and utilities for orchestrator plugins.

Plugins are simple classes that implement a single `run` method.  The
orchestrator instantiates the plugin and calls `run(config, context)`
whenever the corresponding task is executed.  The plugin should perform
whatever work is necessary and return a JSON‑serialisable object that
captures the result.  It may also read and modify the shared `context`
dictionary to pass intermediate outputs to downstream tasks.
"""

from typing import Any, Dict


class Plugin:
    """Base class for orchestrator plugins."""

    #: Unique name used to refer to this plugin in workflow YAML files.
    name: str = "plugin"

    def run(self, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute the plugin.

        Parameters
        ----------
        config:
            A dictionary representing the configuration passed from the
            workflow.  The structure of this dictionary is defined by the
            plugin itself.
        context:
            A shared dictionary containing the results of previously executed
            tasks.  Plugins may use this to inspect upstream results and
            publish their own outputs.

        Returns
        -------
        Any
            A JSON‑serialisable value representing the result of the
            operation.  The orchestrator will record this result under the
            task's ID in the run summary.
        """
        raise NotImplementedError
