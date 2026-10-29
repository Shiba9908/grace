# Atomistic methods

## ASE and ML interatomic potentials

Record potential family and exact checkpoint/hash, package versions, elements,
device, precision, units, stress support, constraints, optimizer, force tolerance,
cell/volume protocol, and random seeds. Keep calculators separate from the ASE
workflow so another potential can be substituted under matched settings.

For relaxation, save final coordinates, energy, maximum force, convergence flag,
and cell, including failed samples. Recompute critical energy differences under
matched precision and references. A surrogate fit's cross-validation error or
within-motif spread is not MLIP-versus-DFT error. Use held-out structures/hosts for
validation and report energy/force/stress errors for the intended domain.

## LAMMPS

LAMMPS is a simulation engine; MACE is a potential. An ASE-versus-LAMMPS comparison
using the same checkpoint checks engine/interface consistency, not independent
agreement between physical models.

Before using an MLIP through LAMMPS, verify the installed interface against its
upstream version-specific documentation, unit style, atom-type/species mapping,
cell/PBC, neighbour settings, constraints, precision, and GPU/MPI support. Compare
single-point energies and forces on the same structures against the Python/ASE
reference. Then check a short appropriate trajectory before production. Do not
copy old pair-style flags or assume a plugin is installed.

## DFT

Check executable/license access and existing site workflow before preparing or
submitting a batch. Record functional, pseudopotential identities, cutoff,
k-point scheme, electronic/ionic convergence, spin/magnetic initialization,
smearing, cell constraints and references. Preserve licensed potentials outside
GitHub. Converge the target property; do not assume any DFT run is ground truth.

Select a small representative validation set spanning motifs, energies,
distortions, migrated/retained cases and outliers. Match atoms/cell/reference
definitions and separate fixed-geometry evaluation from method-specific
relaxation. Check both electronic and ionic convergence.

## Single-H energy convention and optional checker

For one added H and an explicitly selected H2 reference:

`E_insert = E(host+H) - E(host) - 0.5 * E(H2)`.

Host and host+H must follow the stated matched protocol. Do not pool screening,
tight-relaxation and different-volume references silently. Keep ZPE corrections
and finite-temperature free energies as separate named columns. Recompute the
appropriate reference for a changed potential or electronic-structure protocol.

The bundled `scripts/audit_h_insertions.py` consumes normalized JSONL, one record
per sample, with these required fields:

| Field | Meaning |
| --- | --- |
| `sample_id` | Unique nonempty string within this cohort |
| `protocol_id`, `reference_id` | Nonempty IDs that resolve to the actual run record |
| `converged` | JSON boolean; true is required |
| `fmax_ev_a` | Finite nonnegative maximum force in eV/angstrom |
| `energy_host_h_ev`, `energy_host_ev`, `energy_h2_ev` | Finite raw energies in eV |
| `insertion_energy_ev` | Reported electronic insertion energy in eV, without ZPE |
| `structure_path` | Final structure file, relative to the JSONL directory or absolute |

Example invocation (choose tolerances from the run protocol):

```bash
python /path/to/grace-research/scripts/audit_h_insertions.py normalized.jsonl \
  --expected-count 1000 --fmax-limit 0.005 --energy-atol 0.000001
```

Map source columns explicitly and retain the raw source path/row identity; do not
invent missing convergence, forces, coordinates or references. Run where structure
files are available. The checker fails closed for malformed rows, missing files,
duplicate IDs, inconsistent energies, or mixed reference/protocol IDs. Exit 0
means these limited record checks pass; exit 1 means failed checks; exit 2 means
an invocation or file-read error. It does not check geometry, model validity,
reference compatibility, or that the structure matches its claimed energy.

Design reference:
[ASE/MACE adapter](https://github.com/jinzhezenggroup/computational-chemistry-agent-skills/tree/master/atomistic-workflows/ase/ase-calculators/mace).
Use the [upstream MACE ASE guide](https://mace-docs.readthedocs.io/en/latest/guide/ase.html)
for calculator setup, checking it against the installed version.
