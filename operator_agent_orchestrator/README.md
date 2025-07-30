# Operator Agent Orchestrator

An operator‑grade multi‑agent orchestration framework for building repeatable,
auditable workflows.  This project was designed after studying the existing
repositories in the Operator meta portfolio, such as the Job Offer Factory
pipeline【931809230789610†L12-L18】, the Leadscore API【424943483667472†L12-L18】 and the Operator Metrics
Dashboard【241691391405493†L12-L19】.  Those projects share common principles—automation, modularity and
compounding learning—but each solves a very specific problem.  The
Operator Agent Orchestrator generalises those ideas into a reusable engine
for orchestrating heterogeneous tasks.

## Why build this?

The existing Operator tools cover code review, lead scoring, job search,
trading and compliance.  However, each of them implements its own ad‑hoc
task runner.  There is no single place to define a workflow composed of
discrete, re‑usable steps (agents), run them concurrently with dependency
resolution, log their outputs and expose the results for further analysis.

This repository fills that gap.  It lets you define complex workflows in a
declarative YAML format, execute them locally without relying on any cloud
API, and capture the provenance of every step for auditability.  It serves
as a foundation on top of which you can build new vertical applications,
compose existing operator modules or simply automate your own processes.

## Features

- **Declarative workflows** – describe your workflow as a YAML file that
  lists tasks, their configuration and their dependencies.
- **Plugin system** – extend the orchestrator by writing your own
  plugins.  A plugin is a Python class that implements a simple `run`
  method.  Out of the box you get shell execution, Python function
  invocation, CSV ingestion and metric computation.
- **Concurrent execution** – tasks without dependencies run in parallel
  using Python's `asyncio` infrastructure.  Downstream tasks wait for
  their prerequisites to finish.
- **Shared context** – tasks can publish results into a shared context
  dictionary.  Subsequent tasks can read intermediate outputs and
  reuse them.
- **Logging and audit trails** – each workflow run writes a timestamped
  log directory containing structured JSON results for every task and a
  human‑readable summary.  Nothing is hidden.
- **Command‑line interface** – run workflows, list available plugins and
  generate example configuration files using a single `oprun` command.

## Quickstart

1. Install the dependencies (requires Python 3.8+):

   ```sh
   pip install -r requirements.txt
   ```

2. Create a workflow file.  You can copy the example from
   `examples/workflow_example.yaml`:

   ```sh
   cp operator_agent_orchestrator/examples/workflow_example.yaml my_workflow.yaml
   ```

3. Prepare any input files referenced in your workflow (for example
   `examples/sample_data.csv`).

4. Execute the workflow:

   ```sh
   python -m operator_agent_orchestrator my_workflow.yaml
   ```

5. Check the generated `logs/` directory for run summaries and JSON
   outputs.

## Declarative workflow format

A workflow YAML file has the following structure:

```yaml
name: Example Workflow
description: Ingest data and compute metrics
tasks:
  - id: ingest_csv
    plugin: csv_ingest
    config:
      path: examples/sample_data.csv
    depends_on: []
  - id: compute_metrics
    plugin: metrics
    config:
      numeric_columns: [age, score]
    depends_on: [ingest_csv]
  - id: notify
    plugin: shell
    config:
      command: "echo Metrics computed"
    depends_on: [compute_metrics]
```

Every task has an `id`, references a `plugin` and may specify a
configuration dictionary.  The optional `depends_on` list names other task
IDs that must complete before this task runs.

## Extending the orchestrator

Plugins live in the `operator_agent_orchestrator/plugins/` package.  To
create your own plugin, subclass `Plugin` (or implement a `run` method
with the same signature) and add it to the `PLUGINS` dictionary in
`plugins/__init__.py`.  You can access intermediate results via the
`context` parameter and return any JSON‑serialisable value.

For example, a plugin that writes a greeting:

```python
from operator_agent_orchestrator.plugin_base import Plugin

class GreetPlugin(Plugin):
    name = "greet"
    def run(self, config: dict, context: dict) -> dict:
        name = config.get("name", "world")
        message = f"Hello, {name}!"
        return {"message": message}
```

Then add it to `PLUGINS`:

```python
from .greet import GreetPlugin
PLUGINS["greet"] = GreetPlugin
```

## License

This project is licensed under the MIT License.  See `LICENSE` for details.
