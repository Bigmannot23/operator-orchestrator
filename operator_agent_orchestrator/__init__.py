"""Top‑level package alias for the Operator Agent Orchestrator project.

This file exposes the main :class:`Orchestrator` class directly from the
subpackage of the same name so that users can import it as
``from operator_agent_orchestrator import Orchestrator``.
"""

from .operator_agent_orchestrator import Orchestrator  # noqa: F401

# Re‑export nested examples to make ``operator_agent_orchestrator.examples``
# available.  Without this alias, the examples package lives at
# ``operator_agent_orchestrator.operator_agent_orchestrator.examples`` which
# is inconvenient to import from user code.  See the README for usage.
from .operator_agent_orchestrator import examples  # noqa: F401

__all__ = ["Orchestrator", "examples"]