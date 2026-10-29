"""Synthetic record checks; no network, GPU, or real calculation required."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/audit_h_insertions.py"
SPEC = importlib.util.spec_from_file_location("audit_h_insertions", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class RecordChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="grace-audit-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "final.extxyz").write_text("1\nsynthetic fixture\nH 0 0 0\n")
        self.data = self.root / "records.jsonl"
        self.row = dict(
            sample_id="a", protocol_id="p1", reference_id="r1",
            converged=True, fmax_ev_a=0.004, energy_host_h_ev=-104.0,
            energy_host_ev=-100.0, energy_h2_ev=-6.0,
            insertion_energy_ev=-1.0, structure_path="final.extxyz",
        )

    def run_audit(self, rows, expected=1):
        self.data.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
        return AUDIT.audit(self.data, expected, 0.005, 1e-6)

    def test_matched_complete_record(self):
        self.assertTrue(self.run_audit([self.row])["ok"])

    def test_failed_or_unverifiable_records(self):
        for change in (
            {"converged": False}, {"converged": "true"},
            {"fmax_ev_a": 0.006}, {"fmax_ev_a": float("nan")},
            {"fmax_ev_a": True}, {"fmax_ev_a": -1},
            {"energy_host_ev": float("inf")}, {"insertion_energy_ev": 2.0},
            {"structure_path": "absent.xyz"}, {"structure_path": "bad\x00path"},
            {"sample_id": None}, {"protocol_id": ""}, {"reference_id": None},
        ):
            with self.subTest(change=change):
                self.assertFalse(self.run_audit([self.row | change])["ok"])

    def test_duplicates_and_mixed_cohorts(self):
        for second in (
            self.row, self.row | {"sample_id": "b", "reference_id": "r2"},
            self.row | {"sample_id": "b", "protocol_id": "p2"},
        ):
            with self.subTest(second=second):
                self.assertFalse(self.run_audit([self.row, second], 2)["ok"])

    def test_counts_and_invalid_input(self):
        self.assertFalse(self.run_audit([self.row], 2)["ok"])
        self.assertFalse(self.run_audit([])["ok"])
        self.assertFalse(self.run_audit([[]])["ok"])
        self.data.write_text("{broken\n")
        self.assertFalse(AUDIT.audit(self.data, 1, 0.005, 1e-6)["ok"])

    def test_cli_exit_codes(self):
        command = [sys.executable, str(SCRIPT), str(self.data),
                   "--expected-count", "1", "--fmax-limit", "0.005",
                   "--energy-atol", "0.000001"]
        self.run_audit([self.row])
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        self.run_audit([self.row | {"converged": False}])
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 1)
        self.data.unlink()
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
