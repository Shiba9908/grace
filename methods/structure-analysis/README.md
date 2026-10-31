# Bond-length / neighbour-distance analysis

`bond_lengths.py` reads ASE-supported structures, extracts periodic neighbours
inside an explicit cutoff, and writes distributions and shortest distances per
file/frame and element pair. This is geometric analysis; a distance cutoff does
not establish electronic bonding. Histograms are probability densities, **not RDFs**.

Requirements: Python 3.9+, ASE, NumPy; Matplotlib for plots. The existing Grace
MACE environment is expected to provide these; inspect it before installing.

## Run

From the repository root, for the available relaxed 2NN examples:

```bash
python3 methods/structure-analysis/bond_lengths.py \
  '../motifs/2026-10-29-2nn/relaxed-examples/*_relaxed.extxyz' \
  --cutoff 3.5 --out ../reports/bond-lengths-2nn-examples
```

3.5 Å is an illustrative **search range**, not a universal first-neighbour or
bond cutoff. At approximately 3.07 Å BCC lattice parameter it includes multiple
metal-neighbour shells. Inspect distance peaks or an RDF to select shell cutoffs,
and repeat with another cutoff if your scientific definition requires it.

Default: last frame only (`frame_index=-1`). Add `--frames all` for all stored
frames; those use actual zero-based frame indices. For the three-snapshot motif54
visualizations, all frames compare start/middle/end optimizer configurations;
these snapshots are not physical-time MD samples.

```bash
python3 methods/structure-analysis/bond_lengths.py \
  '../motifs/2026-10-26-pilot/visual-check-motif54/*_3snapshots.extxyz' \
  --frames all --cutoff 3.5 --out ../reports/bond-lengths-motif54-snapshots
```

Pass POSCAR/CIF/other ASE-readable files similarly. LAMMPS dump formats may need
`--format lammps-dump-text` and valid species/type mapping in the input; do not
guess elements from numeric type labels. Files lacking a periodic cell/PBC need
those supplied correctly in the source before interpreting crystal distances.
Input files are read only. Output must be a new directory to prevent overwrites.

## Outputs

| File | Contents |
| --- | --- |
| `bonds.csv` | Every retained atom/image edge: indices, elements, image shift and distance in Å |
| `summary.csv` | Per-case/group counts, minimum, mean, population SD, median, maximum, and atom/image identity of one shortest edge |
| `histograms.csv` | Common-bin counts and probability density for each case/group |
| `metadata.json` | Input/code hashes, cutoff, versions, frame selection and complete/failed status |
| `plots/` | PNG and PDF distributions per case; disable with `--no-plots` |

Groups include all neighbours, H–metal, metal–metal, and each present element
combination (e.g. H–V, H–W, H–Ti, H–Cr). In this alloy-focused tool "metal" means
any non-H species; use element-pair rows for systems with other nonmetals.
Empty groups have count zero and blank statistics, **not** a zero minimum.
Population SD describes the listed distances; it is not an error bar from
independent samples. Equally shortest edges are all in `bonds.csv`; summary
identifies one of them.

Periodic counting retains each undirected `(atom_i, atom_j, image_shift)` edge
once and removes its reversed counterpart. Nonzero self-images are real
neighbours in primitive cells, so they are retained. With a large cutoff,
different periodic images of the same atom pair can both be neighbours. This is
not an all-pairs minimum-image distance matrix. All distances are strictly below
the search cutoff, following ASE's neighbour-list convention. A returned minimum
is the shortest distance for that group; if the cutoff finds none, no minimum is
claimed. Do not mix host-only/H-containing, retained/migrated or different
protocols without matching case identities.

## Useful next analyses

1. Compare H–V/H–W/H–Ti/H–Cr distributions across motifs and independent hosts.
2. Compare matched host and host+H metal-pair distances to quantify local distortion.
3. Track initial-to-final distances alongside H migration and final site identity.
4. Relate minimum/mean H–metal distance, coordination and spread to insertion energy,
   retaining host-level splits and convergence filters.
5. Compare the same structures with different MLIPs or matched DFT relaxations.
6. For actual MD trajectories, examine temperature-dependent distances and RDFs;
   use independent blocks/replicas for uncertainty. Distance histograms alone do
   not determine diffusion coefficients.

## Verify

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s methods/structure-analysis/tests -v
```

Tests cover analytic BCC distances, boundary crossing, primitive-cell images,
skew-cell enumeration, duplicate removal, empty groups, histogram normalization,
overlapping atoms and frame selection.

Primary API reference: [ASE neighbour lists](https://docs.ase-lib.org/ase/neighborlist.html).
