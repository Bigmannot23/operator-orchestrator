# Usage Guide

This guide walks you through running workflows with the Operator Agent
Orchestrator and developing your own plugins.

## Installing dependencies

The orchestrator depends on PyYAML, Click and pandas.  These are listed in
`requirements.txt`.  You can install them into a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running a workflow

The simplest way to run a workflow is via the module entrypoint.  Given a
workflow definition:

```yaml
name: hello world
tasks:
  - id: greet
    plugin: shell
    config:
      command: echo Hello, world!
    depends_on: []
```

execute it like this:

```sh
python -m operator_agent_orchestrator path/to/workflow.yaml
```

The orchestrator prints progress to the console and writes logs under
`logs/`.  You can customise the logs directory with the `--log-dir`
option.

Alternatively you can install the package and use the `oprun` script defined
in `pyproject.toml`:

```sh
pip install -e .
oprun run path/to/workflow.yaml
```

## Listing available plugins

To see which plugins are available, run:

```sh
python -m operator_agent_orchestrator list-plugins
```

This command prints the names of all registered plugins.  You can create
additional plugins and register them in `plugins/__init__.py`.

## Copying the example workflow

If you'd like to start from the built‑in example, use the `copy-example`
command:

```sh
python -m operator_agent_orchestrator copy-example my_workflow.yaml
```

This command copies the example YAML from the package into the current
directory.  You can then modify it to suit your needs.

## Developing a plugin

Plugins live in the `operator_agent_orchestrator/plugins/` package.  A
plugin must subclass `Plugin` from `plugin_base.py` and implement a
`run(config, context)` method.  The orchestrator instantiates the plugin
for each task, passing the configuration dictionary and the shared
context.  The plugin must return a JSON‑serialisable value which will be
written to the summary file.

Remember to register your new plugin in `plugins/__init__.py`:

```python
from .my_plugin import MyPlugin
PLUGINS[MyPlugin.name] = MyPlugin
```

### Example plugin

Suppose you want to write a plugin that reverses a string.  Create
``operator_agent_orchestrator/plugins/reverse.py``:

```python
from ..plugin_base import Plugin

class ReversePlugin(Plugin):
    name = "reverse"
    def run(self, config, context):
        text = config.get("text", "")
        return {"reversed": text[::-1]}
```

Then register it:

```python
from .reverse import ReversePlugin
PLUGINS[ReversePlugin.name] = ReversePlugin
```

In your workflow YAML you can now use:

```yaml
tasks:
  - id: rev
    plugin: reverse
    config:
      text: hello
    depends_on: []
```

## Testing your workflows

Unit tests live in the `tests/` directory.  The included tests illustrate
how to programmatically run a workflow and assert on the results.  To run
the tests:

```sh
python -m unittest discover -s tests
```