#!/usr/bin/env python3
"""Select implementation-language candidates from the local profile table.

Reads only. No network, no package installation, no code execution of any
selected language. A match means "worth examining", never "correct choice".

Usage:
    python3 select_profile.py --require memory=manual --require platform=native
    python3 select_profile.py --require memory=gc --require platform=math --json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REQUIRED_FIELDS = ("name", "paradigm", "type-system", "memory", "concurrency",
                   "error-handling", "build", "tests", "lint", "fuzz", "verify",
                   "platform", "notes")
TABLE = Path(__file__).resolve().parent.parent / "references/language-profiles.csv"


def load_profiles(path: Path = TABLE) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"empty profile table: {path}")
    names = [row["name"] for row in rows]
    if len(names) != len(set(names)):
        raise ValueError("duplicate language names in profile table")
    for row in rows:
        missing = [field for field in REQUIRED_FIELDS if field not in row]
        if missing:
            raise ValueError(f"{row.get('name', '?')}: missing fields {missing}")
    return rows


def matches(row: dict[str, str], requirements: dict[str, str]) -> bool:
    """Substring match per requirement.

    `field=value` requires `value` to occur in the field (case-insensitive).
    `field-not=value` requires it not to occur. `field-equals=value` requires an
    exact match. Suffixes let one row express more than one requirement on the
    same field, which is how a genuinely infeasible requirement set is detected.
    """
    for key, wanted in requirements.items():
        if not wanted:
            raise ValueError(f"empty requirement value for {key}")
        negate = key.endswith("-not")
        exact = key.endswith("-equals")
        field = key[:-4] if negate else (key[:-7] if exact else key)
        if field not in row:
            raise ValueError(f"unknown profile field: {field}")
        value = row[field].lower()
        needle = wanted.lower()
        if negate:
            ok = needle not in value
        elif exact:
            ok = needle == value
        else:
            ok = needle in value
        if not ok:
            return False
    return True


def select(requirements: dict[str, str], path: Path = TABLE) -> dict:
    profiles = load_profiles(path)
    matched = sorted(row["name"] for row in profiles if matches(row, requirements))
    return {
        "requirements": requirements,
        "profileCount": len(profiles),
        "matched": matched,
        "status": "candidates" if matched else "infeasible",
    }


def parse_requirement(text: str) -> tuple[str, str]:
    if "=" not in text:
        raise ValueError(f"requirement must be field=value: {text!r}")
    field, _, value = text.partition("=")
    return field.strip(), value.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require", action="append", default=[], metavar="FIELD=VALUE")
    parser.add_argument("--table", type=Path, default=TABLE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        requirements = dict(parse_requirement(item) for item in args.require)
        result = select(requirements, args.table)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"status: {result['status']}  profiles examined: {result['profileCount']}")
        for name in result["matched"]:
            print(f"  {name}")
        if result["status"] == "infeasible":
            print("No profile satisfies every requirement. Relax one deliberately; do not default.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
