"""Composition root (Dependency Injection bootstrap).

This module wires application use cases to concrete implementations of ports.
Adapters should be provided by the outer layers and passed into the builders
here. Keep this module free of business logic; it exists solely to compose.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv

from .ports.storage import TraceStoragePort
from .use_cases import ProcessTraceUseCase


def build_use_cases(storage: TraceStoragePort) -> Dict[str, Any]:
    """Build and return the application use cases.

    Args:
        storage: Concrete implementation of TraceStoragePort.

    Returns:
        A dictionary with instantiated use cases.
    """
    return {
        "process_trace": ProcessTraceUseCase(storage=storage),
    }


def main() -> int:
    """Entrypoint for ``python -m obsvty``.

    Loads environment variables and prints a quick status message.
    Actual adapter wiring should be done by callers that provide concrete
    implementations of the ports to :func:`build_use_cases`.
    """
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        # Attempt project-root .env if running from inside src
        project_env = Path(__file__).resolve().parents[2] / ".env"
        if project_env.exists():
            load_dotenv(dotenv_path=project_env)

    print("obsvty composition root loaded. Provide adapters to build_use_cases().")
    return 0
