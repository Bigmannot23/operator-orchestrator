# Architecture

The Operator Agent Orchestrator consists of three main layers:

1. **Workflow loader** – Parses YAML definitions into internal task
   representations.  YAML was chosen for its readability and ability to
   represent nested configuration.  Each workflow declares a name,
   description and a list of tasks.  Tasks specify a unique ID, the
   plugin used to implement the task, optional configuration and a list of
   dependencies.

2. **Execution engine** – Implements dependency resolution and task
   execution.  The orchestrator uses Python's `asyncio` library to run
   tasks concurrently: every task is scheduled as an `asyncio.Task` whose
   coroutine first awaits all of its dependencies before invoking the
   underlying plugin.  Plugins themselves run synchronously via
   `asyncio.to_thread` so that CPU‑bound work does not block the event
   loop.  Results are collected into a shared context dictionary keyed by
   task ID.  At the end of a run the orchestrator writes a structured
   summary JSON file capturing each task's return value.  All output
   (including exceptions) is also logged to a timestamped log file.

3. **Plugin system** – Plugins provide the concrete implementation for
   tasks.  They are discovered through the `PLUGINS` dictionary in
   `operator_agent_orchestrator/plugins/__init__.py`.  A plugin
   implements a `run(config, context)` method.  The built‑in plugins
   include:
   - `shell` – executes arbitrary shell commands and captures output.
   - `python_function` – dynamically imports and calls a Python
     function specified by module and name.
   - `csv_ingest` – reads a CSV file into a pandas DataFrame and
     publishes it to the shared context.
   - `metrics` – computes statistics for numeric columns of a DataFrame
     stored in the context.

The plugin architecture is intentionally simple: new behaviours can be
implemented by writing a single Python class and registering it in
`PLUGINS`.  Because plugins receive both their own configuration and the
full context of previous task results, they enable powerful patterns
without coupling the orchestrator to specific domains.

## Logging and auditability

Every workflow run generates a unique subdirectory inside the configurable
`logs/` folder.  The directory name includes a timestamp and the base
name of the workflow file.  Within each run directory you will find:

- `run.log` – a human‑readable log of events, including task starts,
  completions and any exceptions raised by plugins.
- `summary.json` – a machine‑readable JSON file mapping task IDs to
  their results.  Values are serialised using `json.dump`.  You can
  feed this into other tools, such as dashboards or further workflows.

By keeping logs and outputs separate for each run, the orchestrator
facilitates traceability and easy audits.  The run directory can be
archived, versioned or attached as evidence in compliance workflows.

## Future extensions

The current implementation demonstrates a minimal viable orchestrator.
Future work could include:

- A web UI built with FastAPI or Starlette to monitor workflows in real
  time.
- Retry policies and error handling strategies (e.g. exponential backoff,
  circuit breakers).
- Persistent context storage via databases or message queues.
- Fine‑grained permissioning for tasks and plugins.
- Integration with the broader Operator meta portfolio, such as
  automatically logging results into the Operator Metrics Dashboard or
  feeding data into the Leadscore API.