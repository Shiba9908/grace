# Grace alloy research

Motif-centred alloy-development workflows for TAMU Grace, covering ASE/MLIP,
LAMMPS, DFT, diffusion, comparisons across methods, and phase-field handoffs.
V–W–Ti–Cr + H is the current case study; the workflow can be extended to other
alloys after checking the lattice, motif definition and model domain.

## Use the research skill

The reusable instructions live in
[`.agents/skills/grace-research/SKILL.md`](.agents/skills/grace-research/SKILL.md).
An agent supporting project skills can discover it from this checkout. In Codex,
use `$grace-research`, for example:

> Use $grace-research to inspect my current motif run, check convergence and
> migration, and identify the next calculation justified by the evidence.

Useful starting points:

| Work | Reference |
| --- | --- |
| Grace environment, Slurm, restart and transfer | [Grace execution](.agents/skills/grace-research/references/grace-execution.md) |
| Motif geometry, symmetry, shell fixing and sampling | [Motifs](.agents/skills/grace-research/references/motifs.md) |
| ASE/MLIP, LAMMPS, DFT and insertion-energy checks | [Atomistic methods](.agents/skills/grace-research/references/atomistic-methods.md) |
| Diffusion, method comparisons and phase-field parameters | [Multiscale work](.agents/skills/grace-research/references/multiscale.md) |
| Run provenance, GitHub and file cleanup | [Records and cleanup](.agents/skills/grace-research/references/records-and-cleanup.md) |

MLIP identifies a potential/model; LAMMPS is a simulation engine that can use a
potential. Comparing ASE and LAMMPS with the same potential checks implementation
consistency. Comparing an MLIP against converged DFT addresses physical accuracy.
Keep those comparisons separate.

## What is implemented

This initial repository contains the research skill, its references, a read-only
normalized single-H insertion checker, and synthetic tests. It does not contain
completed LAMMPS, DFT, diffusion or phase-field simulation pipelines. Those are
workflow directions, not claims of generated results or validated solvers.

Existing research data, scripts and deliverables remain in the organized local
`~/E Drive/mace-grace-setup/` tree and the Grace calculation directory. The local
index and dated run records identify those artifacts. This repository is not a
complete backup of the calculations.

## Check the checker

The checker uses Python 3.9+ and the standard library. From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s .agents/skills/grace-research/tests -v
```

For actual normalized single-H records, supply the expected count and tolerances
from the run protocol:

```bash
python3 .agents/skills/grace-research/scripts/audit_h_insertions.py records.jsonl \
  --expected-count 1000 --fmax-limit 0.005 --energy-atol 0.000001
```

The numbers above illustrate a command; they are not defaults for every study.
Read the [input schema and limits](.agents/skills/grace-research/references/atomistic-methods.md#single-h-energy-convention-and-optional-checker).
Passing checks do not establish model accuracy or correct geometric assignments.

## Keep the repository focused

Track reusable source code, small configurations, methodology, concise run
metadata and representative test fixtures. Add motif/method directories when
they contain actual maintained code; avoid empty trees for future possibilities.

Keep bulk trajectories, result dumps, checkpoints, caches and recovery archives
in research storage, with checksums and paths in run records. Do not commit
credentials or licensed pseudopotentials. Distinguish actual computation outputs
from optimizer trajectories, demonstrations and historical snapshots.

The existing skill describes the Mac/Grace layout. Changing a path in these
instructions does not move the actual Grace calculations. Inspect the current
run manifest and scheduler before restarting work.
