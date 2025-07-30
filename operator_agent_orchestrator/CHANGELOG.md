# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-07-30
### Added
- Initial release of the Operator Agent Orchestrator.
- Declarative workflow YAML format with tasks, plugins and dependencies.
- Built‑in plugins: `shell`, `python_function`, `csv_ingest`, `metrics`.
- Concurrency via `asyncio` with dependency resolution.
- CLI (`oprun`) with commands to run workflows and list plugins.
- Examples, documentation and tests.