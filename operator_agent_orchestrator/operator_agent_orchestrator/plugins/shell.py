"""Shell command plugin.

This plugin executes a shell command defined in the task configuration.
It captures standard output and standard error and returns them as part
of the result.  Use this plugin to run arbitrary shell commands such as
copying files, invoking other scripts or sending simple notifications.
"""

import subprocess
from typing import Any, Dict

from ..plugin_base import Plugin


class ShellPlugin(Plugin):
    """Execute a shell command using ``subprocess``."""

    name = "shell"

    def run(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        command = config.get("command")
        if not command:
            raise ValueError("Shell plugin requires a 'command' in config")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }