#!/usr/bin/env python3
"""Compare Python-generated output against Kotlin reference, with optional astyle normalization.

Usage:
  python3 tools/codegen/python/cmp.py          # astyle-normalized comparison
  python3 tools/codegen/python/cmp.py --raw    # raw byte-for-byte comparison
"""
import argparse
import difflib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generated"))

REPO = Path(os.environ.get("ER_REPO", Path(__file__).resolve().parents[3]))
REFERENCE_REPO = Path(os.environ.get("ER_REFERENCE_REPO", REPO))
ASTYLE_OPTS = ["astyle", "--mode=c", "--indent=spaces=4", "--style=attach",
               "--lineend=linux", "--max-code-length=200", "--suffix=none", "-q", "-Q"]

def generate_all(specs):
    """Generate all files via Python codegen."""
    from codegen_py.load import GameData
    from codegen_py.main import render_generator

    data = GameData(REPO / "proto")
    out_dir = Path(tempfile.mkdtemp(prefix="pycodegen_cmp_"))

    for spec in specs.values():
        out_path = out_dir / spec.output_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(render_generator(spec, data), encoding="utf-8")

    return out_dir


def astyle_normalize(directory: Path):
    """Run astyle on all .h/.hh files in directory."""
    for f in directory.rglob("*.h"):
        subprocess.run(ASTYLE_OPTS + [str(f)], capture_output=True, check=True)
    for f in directory.rglob("*.hh"):
        subprocess.run(ASTYLE_OPTS + [str(f)], capture_output=True, check=True)


def main():
    from codegen_py.main import SPECS

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generators", nargs="*", help="generator names to compare (default: all)")
    parser.add_argument("--raw", action="store_true", help="skip astyle normalization")
    parser.add_argument("--diff", action="store_true", help="print unified diffs")
    args = parser.parse_args()

    unknown = sorted(set(args.generators) - SPECS.keys())
    if unknown:
        parser.error(f"unknown generator(s): {', '.join(unknown)}")
    specs = {name: SPECS[name] for name in args.generators} if args.generators else SPECS
    use_astyle = not args.raw
    if use_astyle and shutil.which("astyle") is None:
        parser.error("astyle is required for normalized comparison")

    mode = "astyle" if use_astyle else "raw"
    print(f"=== Comparing ({mode}) ===\n")

    gen_dir = generate_all(specs)

    if use_astyle:
        # Copy ref, normalize both
        ref_dir = Path(tempfile.mkdtemp(prefix="pycodegen_ref_"))
        shutil.copytree(REFERENCE_REPO / "include/generated", ref_dir / "include/generated")
        shutil.copytree(REFERENCE_REPO / "asm/generated", ref_dir / "asm/generated")
        astyle_normalize(ref_dir)
        astyle_normalize(gen_dir)
        ref_base = ref_dir
    else:
        ref_base = REPO

    exact = 0
    diff_count = 0
    errors = 0
    total_lines = 0

    for gen_type, spec in sorted(specs.items()):
        gen_file = gen_dir / spec.output_path
        if use_astyle:
            ref_file = ref_base / spec.output_path
        else:
            ref_file = REFERENCE_REPO / spec.output_path

        if not gen_file.exists():
            print(f"  ERROR  {gen_type:30s} (not generated)")
            errors += 1
            continue

        gen_text = gen_file.read_text()
        gen_lines = gen_text.count("\n")
        total_lines += gen_lines

        if not ref_file.exists():
            print(f"  SKIP   {gen_type:30s} (no reference)")
            continue

        ref_text = ref_file.read_text()

        if gen_text == ref_text:
            print(f"  EXACT  {gen_type:30s} ({gen_lines} lines)")
            exact += 1
        else:
            gl = gen_text.split("\n")
            rl = ref_text.split("\n")
            matching = sum(1 for a, b in zip(gl, rl) if a == b)
            total_cmp = min(len(gl), len(rl))
            pct = 100 * matching / total_cmp if total_cmp > 0 else 0
            print(f"  DIFF   {gen_type:30s} {matching}/{total_cmp} lines ({pct:.0f}%)")
            if args.diff:
                diff = difflib.unified_diff(
                    ref_text.splitlines(),
                    gen_text.splitlines(),
                    fromfile=f"reference/{spec.output_path}",
                    tofile=f"python/{spec.output_path}",
                    lineterm="",
                )
                print("\n".join(diff))
            diff_count += 1

    print(f"\n{'='*70}")
    print(f"{'Astyle-normalized' if use_astyle else 'Raw byte-for-byte'}: Exact={exact}/{len(specs)}  Diff={diff_count}  Errors={errors}")
    print(f"Total lines: {total_lines}")

    # Cleanup
    shutil.rmtree(gen_dir, ignore_errors=True)
    if use_astyle:
        shutil.rmtree(ref_base, ignore_errors=True)
    return 1 if diff_count or errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
