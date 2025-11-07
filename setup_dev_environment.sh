#!/usr/bin/env bash
set -euo pipefail

echo "[setup] Starting development environment setup..."

# Check Python version >= 3.11
PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")') || true
if [[ -z "${PY_VERSION}" ]]; then
  echo "[setup] Python not found. Please install Python 3.11+." >&2
  exit 1
fi
REQUIRED_MAJOR=3
REQUIRED_MINOR=11
CUR_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
CUR_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
if (( CUR_MAJOR < REQUIRED_MAJOR || (CUR_MAJOR == REQUIRED_MAJOR && CUR_MINOR < REQUIRED_MINOR) )); then
  echo "[setup] Python $PY_VERSION detected, but 3.11+ is required." >&2
  exit 1
fi

# Ensure Poetry is installed
if ! command -v poetry >/dev/null 2>&1; then
  echo "[setup] Poetry not found. Installing..."
  python3 -m pip install --user poetry==1.7.1
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "[setup] Installing dependencies with Poetry..."
poetry install --no-interaction --no-ansi

echo "[setup] Generating OTLP proto stubs..."
python3 generate_protos.py --ref "${OTLP_PROTO_REF:-main}"

echo "[setup] Running lint, typecheck, and tests..."
poetry run tox

echo "[setup] Running security checks..."
poetry run tox -e security || echo "[setup] Security checks reported issues. Review above output."

echo "[setup] Development environment setup complete. ✅"