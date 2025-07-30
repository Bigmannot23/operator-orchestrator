"""Python function invocation plugin.

This plugin dynamically imports and executes a Python function specified by
module path and function name.  It is useful for delegating complex logic
into reusable functions without writing a new plugin.  The function may
return any JSON‑serialisable value.

Configuration schema:

```
plugin: python_function
config:
  function: "path.to.module:function_name"
  args: [arg1, arg2, ...]       # optional positional arguments
  kwargs: {key: value, ...}     # optional keyword arguments
```
"""

import importlib
from typing import Any, Dict, List

from ..plugin_base import Plugin


class PythonFunctionPlugin(Plugin):
    """Call a user‑defined Python function."""

    name = "python_function"

    def run(self, config: Dict[str, Any], context: Dict[str, Any]) -> Any:
        function_path = config.get("function")
        if not function_path or ":" not in function_path:
            raise ValueError(
                "python_function plugin requires 'function' in format 'module.submodule:function_name'"
            )
        module_name, func_name = function_path.split(":", 1)
        try:
            module = importlib.import_module(module_name)
        except ImportError as exc:
            raise ImportError(f"Could not import module '{module_name}': {exc}") from exc
        if not hasattr(module, func_name):
            raise AttributeError(f"Module '{module_name}' has no attribute '{func_name}'")
        func = getattr(module, func_name)
        args: List[Any] = config.get("args", [])
        kwargs: Dict[str, Any] = config.get("kwargs", {})
        return func(*args, **kwargs)