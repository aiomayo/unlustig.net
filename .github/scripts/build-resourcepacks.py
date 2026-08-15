#!/usr/bin/env python3
"""Zip each resourcepacks/<name>/ source tree into resourcepacks/<name>.zip."""

import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACKS = ROOT / "resourcepacks"

FIXED_DATE = (1980, 1, 1, 0, 0, 0)


def build(src: pathlib.Path) -> pathlib.Path:
    out = src.parent / f"{src.name}.zip"

    if not (src / "pack.mcmeta").is_file():
        sys.exit(f"::error::{src.relative_to(ROOT)} has no pack.mcmeta")

    files = sorted(p for p in src.rglob("*") if p.is_file())
    if not files:
        sys.exit(f"::error::{src.relative_to(ROOT)} is empty")

    tmp = out.parent / f"{out.name}.tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for path in files:
            info = zipfile.ZipInfo(
                str(path.relative_to(src).as_posix()), date_time=FIXED_DATE
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes())
    tmp.replace(out)

    print(f"built {out.relative_to(ROOT)} ({out.stat().st_size} bytes, {len(files)} files)")
    return out


def main() -> None:
    if not PACKS.is_dir():
        print("no resourcepacks/ directory, nothing to build")
        return

    sources = sorted(p for p in PACKS.iterdir() if p.is_dir())
    if not sources:
        print("no resource pack sources, nothing to build")
        return

    for src in sources:
        build(src)


if __name__ == "__main__":
    main()
