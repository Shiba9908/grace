"""Analytic and independent periodic-geometry checks."""
import importlib.util
import itertools
from pathlib import Path
import tempfile
import unittest

from ase import Atoms
from ase.build import bulk
from ase.io import write
import numpy as np

SCRIPT = Path(__file__).resolve().parents[1] / "bond_lengths.py"
SPEC = importlib.util.spec_from_file_location("bond_lengths", SCRIPT)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class GeometryChecks(unittest.TestCase):
    def test_nonperiodic_dimer_and_empty_groups(self):
        atoms = Atoms("VH", positions=[[0, 0, 0], [1.7, 0, 0]])
        bonds = MOD.extract_bonds(atoms, 2.0)
        self.assertEqual(len(bonds), 1)
        self.assertAlmostEqual(bonds[0]["distance_A"], 1.7)
        groups = MOD.groups_for(atoms, bonds)
        self.assertEqual(len(groups["H-V"]), 1)
        self.assertIsNone(MOD.summary(groups["metal-metal"])["min_A"])

    def test_boundary_crossing(self):
        atoms = Atoms("VH", positions=[[0.1, 0, 0], [9.9, 0, 0]], cell=[10]*3, pbc=True)
        bonds = MOD.extract_bonds(atoms, 0.5)
        self.assertEqual(len(bonds), 1)
        self.assertAlmostEqual(bonds[0]["distance_A"], 0.2)
        self.assertNotEqual(bonds[0]["shift_x"], 0)

    def test_bcc_analytic_neighbours(self):
        atoms = bulk("W", "bcc", a=3.0, cubic=True)
        bonds = MOD.extract_bonds(atoms, 2.7)
        self.assertEqual(len(bonds), 8)  # two atoms x 8 neighbours / 2
        np.testing.assert_allclose([b["distance_A"] for b in bonds], 3*np.sqrt(3)/2)

    def test_periodic_self_images_are_real_edges(self):
        atoms = Atoms("H", positions=[[0, 0, 0]], cell=[1]*3, pbc=True)
        bonds = MOD.extract_bonds(atoms, 1.1)
        self.assertEqual(len(bonds), 3)  # six directed neighbours / 2
        self.assertEqual(len(MOD.groups_for(atoms, bonds)["H-H"]), 3)
        self.assertTrue(all(b["distance_A"] == 1 for b in bonds))

    def test_skew_cell_against_independent_image_enumeration(self):
        atoms = Atoms("VTiH", scaled_positions=[[.1,.2,.3],[.8,.1,.6],[.4,.7,.2]],
                      cell=[[3,0,0],[1.1,2.8,0],[.3,.6,3.1]], pbc=True)
        cutoff = 2.3
        expected = []
        for i in range(len(atoms)):
            for j in range(len(atoms)):
                for shift in itertools.product(range(-2, 3), repeat=3):
                    if i == j and shift == (0,0,0):
                        continue
                    # Independent half-space ordering, not canonical_edge().
                    if (i, j, *shift) > (j, i, *(-x for x in shift)):
                        continue
                    d = np.linalg.norm(atoms.positions[j] - atoms.positions[i] + np.array(shift) @ atoms.cell.array)
                    if d < cutoff:
                        expected.append(d)
        measured = [b["distance_A"] for b in MOD.extract_bonds(atoms, cutoff)]
        np.testing.assert_allclose(sorted(measured), sorted(expected), atol=1e-12)
        atoms.positions[1] += atoms.cell[0] - 2*atoms.cell[1]
        np.testing.assert_allclose(sorted(measured), sorted(b["distance_A"] for b in MOD.extract_bonds(atoms, cutoff)))

    def test_histogram_normalization_and_no_neighbours(self):
        atoms = Atoms("VH", positions=[[0, 0, 0], [1.7, 0, 0]])
        bonds = MOD.extract_bonds(atoms, 2)
        edges = np.linspace(0, 2, 21)
        counts, density = MOD.histogram(bonds, edges)
        self.assertEqual(sum(counts), 1)
        self.assertAlmostEqual(float(np.sum(density*np.diff(edges))), 1)
        self.assertEqual(MOD.extract_bonds(atoms, 1), [])
        self.assertIsNone(MOD.summary([])["min_A"])

    def test_overlap_fails(self):
        with self.assertRaises(ValueError):
            MOD.extract_bonds(Atoms("HH", positions=[[0,0,0],[0,0,0]]), 1)

    def test_cli_last_and_all_frames(self):
        import csv
        import json
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "frames.extxyz"
            write(source, [Atoms("VH", positions=[[0,0,0],[d,0,0]]) for d in (1.5, 1.8)])
            for frames, expected in (("last", 1), ("all", 2)):
                out = root / frames
                MOD.main([str(source), "--cutoff", "2", "--frames", frames,
                          "--out", str(out), "--no-plots"])
                self.assertEqual(json.loads((out/"metadata.json").read_text())["cases"], expected)
                with (out/"summary.csv").open() as stream:
                    rows = [r for r in csv.DictReader(stream) if r["group"] == "all"]
                self.assertEqual(len(rows), expected)
                self.assertAlmostEqual(float(rows[-1]["min_A"]), 1.8)
            with self.assertRaises(SystemExit):
                MOD.main([str(source), "--cutoff", "2", "--out", str(root/"last"), "--no-plots"])


if __name__ == "__main__":
    unittest.main()
