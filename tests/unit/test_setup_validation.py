"""Setup validation tests for initial OTLP/gRPC project structure.

These tests validate:
- Directory structure existence (proto and generated folders)
- Pinned dependency versions in pyproject.toml
- Proto download and stub generation (requires grpc_tools)
- Dockerfile presence (build test can be added in CI)
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src/obsvty"
ADAPTERS_MESSAGING = SRC_ROOT / "adapters/messaging"
PROTO_DIR = ADAPTERS_MESSAGING / "proto"
GENERATED_DIR = ADAPTERS_MESSAGING / "generated"


def test_directories_exist():
    assert PROTO_DIR.exists() and PROTO_DIR.is_dir()
    assert GENERATED_DIR.exists() and GENERATED_DIR.is_dir()


def test_pyproject_has_pinned_versions():
    import tomllib  # Python 3.11+

    pyproject = PROJECT_ROOT / "pyproject.toml"
    data = tomllib.loads(pyproject.read_text())
    deps = data["tool"]["poetry"]["dependencies"]
    dev_deps = data["tool"]["poetry"]["group"]["dev"]["dependencies"]

    def _is_pinned(v: str) -> bool:
        # No carets, ranges, or inequality operators
        return all(x not in v for x in ("^", ">", "<", "~", "*"))

    # Check key dependencies pinned
    for pkg in [
        "fastapi",
        "uvicorn",
        "pydantic",
        "grpcio",
        "grpcio-tools",
        "python-dotenv",
        "protobuf",
    ]:
        assert pkg in deps, f"missing dependency: {pkg}"
        assert _is_pinned(str(deps[pkg])), f"{pkg} must be pinned"

    # Dev deps pinned
    for pkg in [
        "pytest",
        "pytest-cov",
        "ruff",
        "mypy",
        "invoke",
        "factory-boy",
        "testcontainers",
        "safety",
        "pre-commit",
    ]:
        assert pkg in dev_deps, f"missing dev dependency: {pkg}"
        assert _is_pinned(str(dev_deps[pkg])), f"{pkg} must be pinned"


def test_protos_generation_creates_python_files():
    pytest = __import__("pytest")
    pytest.importorskip("grpc_tools")

    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "generate_protos.py")], check=True
    )

    assert (GENERATED_DIR / "opentelemetry/proto/common/v1/common_pb2.py").exists()
    assert (GENERATED_DIR / "opentelemetry/proto/resource/v1/resource_pb2.py").exists()
    assert (GENERATED_DIR / "opentelemetry/proto/trace/v1/trace_pb2.py").exists()


def test_dockerfile_exists():
    dockerfile = PROJECT_ROOT / "Dockerfile"
    assert dockerfile.exists(), "Dockerfile should exist in project root"
