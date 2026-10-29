---
name: grace-research
description: Run and review Shib's Grace alloy-research workflows and their MACE-calculations repository or local E Drive mirror, including chemical motifs, ASE/MLIP, LAMMPS, DFT, diffusion, method comparisons, and phase-field handoffs. Use for this research project; exclude unrelated cluster administration and coursework.
---

# Grace alloy research

Support Shib's alloy-development research on TAMU Grace. Chemical motifs and their
relationship to properties are the organizing theme; V–W–Ti–Cr + H is the current
case study, not a restriction on elements, crystal structures, or future methods.
Explain consequential commands and scientific choices as the work proceeds.

## Start from evidence

- Identify whether the request is for planning, preparation, execution, diagnosis,
  analysis, comparison, or cleanup. Complete only the requested scope.
- Read project instructions and the current run record. On Shib's Mac, consult
  `~/AI-Shared/open-items.md` and the latest relevant `~/AI-Shared/log.md` entries.
  Distinguish dated notes, inspected local files, and live Grace evidence.
- Inspect repository identity, branch, status, and applicable instructions before
  editing. A downloaded snapshot is not automatically the active code checkout.
- Check recent edits and running jobs before modifying shared inputs or outputs.
  Coordinate with an active Grace-Claude session; do not overwrite concurrent work.
- Load only the references relevant to the task below. Do not read all datasets
  or recursively search Grace scratch to rediscover known paths.

## Workflows

| Task | Read |
| --- | --- |
| Connect, prepare environments, submit/monitor/recover jobs | [Grace execution](references/grace-execution.md) |
| Build/classify motifs, fix shells, sample alloy environments | [Motifs](references/motifs.md) |
| ASE/MACE, other MLIPs, LAMMPS, or DFT calculations | [Atomistic methods](references/atomistic-methods.md) |
| Diffusion, comparison across methods, or phase-field inputs | [Multiscale work](references/multiscale.md) |
| Provenance, GitHub integration, file organization, cleanup | [Records and cleanup](references/records-and-cleanup.md) |

## Execution and interpretation

- Use the existing verified environment and site settings. Put substantial
  calculations on Slurm compute nodes. An environment import or smoke test is not
  scientific validation of a potential.
- For a new batch, freeze its code/configuration and stable sample-to-task mapping;
  verify a small representative pilot before expanding. A request to inspect
  status does not authorize launching another batch.
- Recover failed or incomplete samples selectively. Diagnose before retrying;
  stop after two retries of the same failure, or at a user-specified limit, and
  report the blocker. Do not silently increase resource use or alter the protocol.
- Require scientific convergence and complete records as well as scheduler
  success. Separate excluded samples and their reasons from the analysis cohort.
- Preserve initial and final identities: motif, geometry, site, and host. Do not
  infer distinct basins from matching energy/chemistry alone.
- Keep raw energies, referenced energies, ZPE corrections, and finite-temperature
  quantities separate. Verify definitions and units before pooling results.
- Treat unpublished results as project data. Linking this skill to GitHub does not
  authorize uploading bulk datasets, model checkpoints, credentials, or licensed
  pseudopotentials, changing repository visibility, or publishing scientific claims.

## Finish

Report what changed, checks performed, output paths, and remaining limitations.
Include job IDs when relevant and state whether results were locally inspected or
verified on Grace. Update the run record and shared log/handoff according to the
project instructions. Leave a single next-step entry instead of creating repeated
status documents. Do not send email or Slack messages.

For normalized **single-H insertion** records, the read-only checker
`scripts/audit_h_insertions.py` checks completeness, force convergence, energy
arithmetic, and matched protocol/reference IDs. See its schema in
[Atomistic methods](references/atomistic-methods.md). It does not validate an MLIP,
classify geometry, or certify DFT/MD/phase-field results.
