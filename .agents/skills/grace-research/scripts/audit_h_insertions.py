#!/usr/bin/env python3
"""Read-only checks of normalized single-H insertion JSONL; stdlib only."""

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import sys


ENERGIES = (
    "energy_host_h_ev", "energy_host_ev", "energy_h2_ev", "insertion_energy_ev"
)


def finite_number(value):
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def audit(path, expected_count, fmax_limit, energy_atol):
    path = Path(path)
    issues = []
    ids = Counter()
    protocols = set()
    references = set()
    count = 0
    passing = 0

    def issue(line, sample_id, reasons):
        issues.append({"line": line, "sample_id": sample_id, "reasons": reasons})

    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            count += 1
            try:
                row = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                issue(line_number, None, ["invalid JSON"])
                continue
            if not isinstance(row, dict):
                issue(line_number, None, ["record must be an object"])
                continue
            reasons = []
            sample_id = row.get("sample_id")
            if not isinstance(sample_id, str) or not sample_id.strip():
                reasons.append("missing/non-string sample_id")
                sample_id = None
            else:
                ids[sample_id] += 1
            for key, seen in (("protocol_id", protocols), ("reference_id", references)):
                value = row.get(key)
                if not isinstance(value, str) or not value.strip():
                    reasons.append("missing/non-string " + key)
                else:
                    seen.add(value)
            if row.get("converged") is not True:
                reasons.append("converged must be boolean true")
            fmax = row.get("fmax_ev_a")
            if not finite_number(fmax) or fmax < 0:
                reasons.append("missing/invalid fmax_ev_a")
            elif fmax > fmax_limit:
                reasons.append("force exceeds protocol limit")
            valid_energies = all(finite_number(row.get(key)) for key in ENERGIES)
            if not valid_energies:
                reasons.append("missing/nonfinite/non-numeric energy")
            else:
                calculated = (
                    row["energy_host_h_ev"] - row["energy_host_ev"]
                    - 0.5 * row["energy_h2_ev"]
                )
                if not math.isfinite(calculated) or not math.isclose(
                    calculated, row["insertion_energy_ev"],
                    rel_tol=0.0, abs_tol=energy_atol,
                ):
                    reasons.append("insertion energy arithmetic mismatch")
            structure = row.get("structure_path")
            if not isinstance(structure, str) or not structure.strip():
                reasons.append("missing/non-string structure_path")
            else:
                structure_path = Path(structure)
                if not structure_path.is_absolute():
                    structure_path = path.parent / structure_path
                try:
                    if not structure_path.is_file() or structure_path.stat().st_size == 0:
                        reasons.append("final structure missing or empty")
                except (OSError, ValueError):
                    reasons.append("invalid/inaccessible structure_path")
            if reasons:
                issue(line_number, sample_id, reasons)
            else:
                passing += 1

    cohort_issues = []
    if count != expected_count:
        cohort_issues.append("record count differs from expected count")
    duplicates = sorted(key for key, value in ids.items() if value > 1)
    if duplicates:
        cohort_issues.append("duplicate sample IDs")
    if len(protocols) > 1:
        cohort_issues.append("mixed protocol IDs; split into matched cohorts")
    if len(references) > 1:
        cohort_issues.append("mixed reference IDs; split into matched cohorts")
    ok = not issues and not cohort_issues
    return {
        "ok": ok,
        "scope": "normalized single-H electronic insertion records only",
        "records": count,
        "expected_count": expected_count,
        "individually_passing_records": passing,
        "cohort_issues": cohort_issues,
        "duplicate_sample_ids": duplicates,
        "protocol_ids": sorted(protocols),
        "reference_ids": sorted(references),
        "record_issues": issues,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("--expected-count", type=int, required=True)
    parser.add_argument("--fmax-limit", type=float, required=True)
    parser.add_argument("--energy-atol", type=float, required=True)
    args = parser.parse_args()
    if args.expected_count <= 0:
        parser.error("--expected-count must be positive")
    if not math.isfinite(args.fmax_limit) or args.fmax_limit <= 0:
        parser.error("--fmax-limit must be finite and positive")
    if not math.isfinite(args.energy_atol) or args.energy_atol < 0:
        parser.error("--energy-atol must be finite and nonnegative")
    try:
        result = audit(args.jsonl, args.expected_count, args.fmax_limit, args.energy_atol)
    except (OSError, UnicodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
