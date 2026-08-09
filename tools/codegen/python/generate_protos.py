#!/usr/bin/env python3
"""Regenerate or verify the committed Python protobuf bindings."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROTO_DIR = ROOT / "proto"
OUTPUT_DIR = Path(__file__).resolve().parent / "generated"
MANIFEST = "manifest.json"


def schema_hashes() -> dict[str, str]:
    return {
        path.relative_to(PROTO_DIR).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(PROTO_DIR.rglob("*.proto"))
    }


def find_protoc(argument: str | None) -> str:
    candidates = [argument, str(ROOT / "tools/codegen/protoc"), shutil.which("protoc")]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return candidate
    raise SystemExit("protoc not found; pass --protoc or place it at tools/codegen/protoc")


def generate(output: Path, protoc: str) -> None:
    output.mkdir(parents=True, exist_ok=True)
    sources = sorted(PROTO_DIR.glob("*.proto"))
    subprocess.run(
        [
            protoc,
            f"--proto_path={PROTO_DIR}",
            f"--python_out={output}",
            f"--pyi_out={output}",
            "--experimental_allow_proto3_optional",
            *(str(path) for path in sources),
        ],
        check=True,
    )
    version = subprocess.run([protoc, "--version"], check=True, capture_output=True, text=True).stdout.strip()
    (output / MANIFEST).write_text(
        json.dumps({"protoc": version, "schemas": schema_hashes()}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def files(path: Path) -> dict[str, bytes]:
    return {
        file.relative_to(path).as_posix(): file.read_bytes()
        for file in sorted(path.rglob("*"))
        if file.is_file() and (file.name.endswith(("_pb2.py", "_pb2.pyi")) or file.name == MANIFEST)
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if committed bindings are stale")
    parser.add_argument("--protoc", help="path to protoc")
    args = parser.parse_args()
    protoc = find_protoc(args.protoc)

    if not args.check:
        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
        generate(OUTPUT_DIR, protoc)
        return 0

    with tempfile.TemporaryDirectory(prefix="eliteredux_pb2_") as temporary:
        generated = Path(temporary)
        generate(generated, protoc)
        expected = files(generated)
        actual = files(OUTPUT_DIR)
        if actual != expected:
            changed = sorted(name for name in actual.keys() | expected.keys() if actual.get(name) != expected.get(name))
            print("Committed protobuf bindings are stale:")
            for name in changed:
                print(f"  {name}")
            print("Run: make -C tools/codegen protos")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
