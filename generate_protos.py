"""Generate gRPC Python stubs from official OpenTelemetry OTLP .proto files.

Idempotent script: downloads OTLP proto (branch/tag configurable), securely
copies required files (common/v1, resource/v1, trace/v1) into
`src/obsvty/adapters/messaging/proto`, and generates Python stubs into
`src/obsvty/adapters/messaging/generated` using ``grpc_tools.protoc``.

Security enhancements:
- Input validation for ``--ref`` (allowed chars: A–Z, a–z, 0–9, . _ -)
- Network timeout with size guard (default 20s, max 50 MiB)
- Safe ZIP processing (prevents path traversal; only copies required folders)

Usage:
  python generate_protos.py --ref <branch-or-tag> [--force] [--timeout 20]

Environment:
  OTLP_PROTO_REF: optional, branch/tag to fetch (default: main)
"""

from __future__ import annotations

import argparse
import io
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path
import re
from zipfile import ZipFile


LOGGER = logging.getLogger("generate_protos")
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

REPO = "open-telemetry/opentelemetry-proto"
BRANCH_ZIP = "https://github.com/{repo}/archive/refs/heads/{ref}.zip"
TAG_ZIP = "https://github.com/{repo}/archive/refs/tags/{ref}.zip"
MAX_ZIP_BYTES = 50 * 1024 * 1024  # 50 MiB safety guard
REF_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


def _download_zip(ref: str, timeout: float) -> bytes:
    import urllib.request

    if not REF_PATTERN.match(ref):
        raise ValueError("Invalid ref: only letters, digits, ._- allowed (max 64)")

    # Prefer tag archive, fallback to branch
    urls = [
        TAG_ZIP.format(repo=REPO, ref=ref),
        BRANCH_ZIP.format(repo=REPO, ref=ref),
    ]
    last_err: Exception | None = None
    for url in urls:
        try:
            LOGGER.info(f"Downloading archive: {url}")
            req = urllib.request.Request(url, headers={"User-Agent": "obsvty-proto-fetch/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                length = r.getheader("Content-Length")
                if length is not None and int(length) > MAX_ZIP_BYTES:
                    raise RuntimeError("Archive too large; aborting")
                data = r.read()
                if len(data) > MAX_ZIP_BYTES:
                    raise RuntimeError("Archive exceeded max size; aborting")
                # Basic zip signature check; full validation happens on ZipFile open
                if not data.startswith(b"PK"):
                    raise RuntimeError("Downloaded file does not look like a ZIP archive")
                return data
        except Exception as e:  # noqa: BLE001 - we log and retry
            last_err = e
            LOGGER.warning(f"Failed to fetch {url}: {e}")
            continue
    assert last_err is not None
    raise RuntimeError(f"Unable to download proto archive: {last_err}")


def _safe_write_member(z: ZipFile, member_name: str, dest_path: Path) -> None:
    # Prevent absolute paths and traversal
    norm = member_name.replace("\\", "/")
    if norm.startswith("/") or ".." in norm:
        raise RuntimeError(f"Unsafe path in ZIP: {member_name}")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with z.open(member_name, "r") as src, open(dest_path, "wb") as out:
        shutil.copyfileobj(src, out)


def _extract_required(src_zip_bytes: bytes, dest_proto_dir: Path) -> Path:
    """Copy only required proto folders from the ZIP into dest.

    Returns the base ``dest_proto_dir / 'opentelemetry' / 'proto'`` path.
    """
    required = [
        ("common", "v1"),
        ("resource", "v1"),
        ("trace", "v1"),
    ]
    base = dest_proto_dir / "opentelemetry" / "proto"
    with ZipFile(io.BytesIO(src_zip_bytes)) as z:
        names = z.namelist()
        # Filter and copy only required directories/files
        for name in names:
            norm = name.replace("\\", "/")
            # We expect a path like: <root>/opentelemetry/proto/<name>/<ver>/...
            if "/opentelemetry/proto/" not in norm:
                continue
            after = norm.split("/opentelemetry/proto/", 1)[1]
            for part, ver in required:
                prefix = f"{part}/{ver}/"
                if after.startswith(prefix):
                    dest = base / after
                    if name.endswith("/"):
                        dest.mkdir(parents=True, exist_ok=True)
                    else:
                        _safe_write_member(z, name, dest)
        # Basic validation: ensure required directories exist
        for part, ver in required:
            if not (base / part / ver).exists():
                raise RuntimeError(f"Missing required proto folder: {part}/{ver}")
    return base


def _reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _generate_stubs(proto_dir: Path, generated_dir: Path) -> None:
    from grpc_tools import protoc

    generated_dir.mkdir(parents=True, exist_ok=True)
    files = [
        "opentelemetry/proto/common/v1/common.proto",
        "opentelemetry/proto/resource/v1/resource.proto",
        "opentelemetry/proto/trace/v1/trace.proto",
    ]
    args = [
        "protoc",
        f"--proto_path={proto_dir}",
        f"--python_out={generated_dir}",
        f"--grpc_python_out={generated_dir}",
        *files,
    ]
    LOGGER.info("Generating Python stubs with grpc_tools.protoc...")
    if protoc.main(args) != 0:
        raise RuntimeError("grpc_tools.protoc failed")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate OTLP gRPC stubs")
    parser.add_argument("--ref", default=os.getenv("OTLP_PROTO_REF", "main"), help="Branch or tag to fetch")
    parser.add_argument("--force", action="store_true", help="Force re-download and regeneration")
    parser.add_argument("--timeout", type=float, default=20.0, help="Network timeout (seconds)")
    args = parser.parse_args()

    project_root = Path(__file__).parent
    proto_dir = project_root / "src/obsvty/adapters/messaging/proto"
    generated_dir = project_root / "src/obsvty/adapters/messaging/generated"
    proto_dir.mkdir(parents=True, exist_ok=True)
    generated_dir.mkdir(parents=True, exist_ok=True)

    # Short-circuit if stubs exist and not forcing
    existing_stub = generated_dir / "opentelemetry/proto/trace/v1/trace_pb2.py"
    if existing_stub.exists() and not args.force:
        LOGGER.info("Stubs already present; use --force to regenerate.")
        return 0

    with tempfile.TemporaryDirectory() as td:
        temp_dir = Path(td)
        zip_bytes = _download_zip(args.ref, timeout=args.timeout)
        # Reset proto dir before copying to avoid stale files
        _reset_dir(proto_dir)
        _extract_required(zip_bytes, proto_dir)
        _generate_stubs(proto_dir, generated_dir)

    LOGGER.info("OTLP proto files downloaded and stubs generated successfully.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        LOGGER.error(f"Failed to generate protos: {e}")
        raise SystemExit(1)