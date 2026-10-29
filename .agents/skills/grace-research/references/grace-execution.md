# Grace execution

## Known locations, verified historically; recheck before use

- SSH alias: `grace` (Shib authenticates interactively/Duo when needed).
- Current H-alloy project: `/scratch/user/shiba/mace-project/vwticr_h`.
- Environment entrypoint: `/scratch/user/shiba/mace-project/enter-mace.sh`.
- Python environment: `/scratch/user/shiba/envs/mace-py311`.
- Local research mirror: `~/E Drive/mace-grace-setup`.
- Existing home backup: `/home/shiba/mace-project-backup`; verify its contents
  and timestamp rather than assuming every new run is backed up.

The locally saved entrypoint loads GCC/13.2.0, OpenMPI/4.1.6, PyTorch/2.7.0,
and WebProxy, activates the environment, and **changes directory to the parent
`mace-project`**. After sourcing it, explicitly enter the intended calculation
directory. These are historical settings, not instructions to reinstall software.
MACE 0.3.16 and MPA-0 medium were recorded in earlier work; inspect the actual
package and model checkpoint/hash for each new protocol.

## Connection and inspection

Use a bounded `ssh -o BatchMode=yes -o ConnectTimeout=15 grace ...` check.
If authentication fails, report that a fresh user login is needed; do not loop,
alter SSH configuration, or claim that a local mirror proves current job status.
Reuse existing connection sharing. Do not install another agent on Grace merely
to use this skill; Codex was removed from Grace on 2026-10-21 after quota issues.

Start with the known project directory and narrowly scoped `git status`, current
instructions, `squeue -u "$USER"`, and explicit job-ID `sacct` queries. Use
`JobID,JobName,State,ExitCode,Elapsed,MaxRSS,AllocTRES` for job accounting where
supported. Avoid exporting full environments or reading credential files.

## Prepare and submit

1. Confirm account/partition/GPU availability, time limits, memory, CPU threading,
   and the project's current batch convention from live settings/site docs.
   A historical smoke test used `gpu`, `gpu:a100:1`, one task, and two CPUs;
   do not turn that example into the resource request for every calculation.
2. Preserve a manifest with code commit or code-file hashes, config hash, input
   identities, environment/model, seeds, protocol, and expected task count.
3. Make the executable work directory explicit and create its log directory before
   submission. `sbatch` stages its script, not every neighbouring file.
4. Run a representative pilot including likely edge cases. Verify real outputs
   and force/solver convergence, then scale within the requested scope.
5. Record the `sbatch --parsable` ID and map array indices to frozen inputs.
   Do not edit code/configuration being used by pending or running tasks.

## Monitoring and recovery

Check scheduler state and exit codes, then actual output completeness and
scientific checks. An existing file can be truncated or belong to an old protocol;
its existence alone is not a completion marker. Preserve failed attempt logs and
resubmit only missing/failed samples after diagnosis. Do not cancel unrelated jobs
or overwrite successful outputs. Keep attempt number and parent job ID.

Use requested status checks or modest checks tied to a running task; a skill is
not a background scheduler. Persistent monitoring needs an actual runner and an
explicitly requested schedule.

For transfers, use selected paths and an rsync dry run, without `--delete` by
default. Verify sizes/checksums and record local/remote direction. Check disk and
file-count quotas before environment installs or large exports.

## Site authority

Confirm changing policy and scheduler details against TAMU HPRC:
- [Grace guide](https://hprc.tamu.edu/kb/User-Guides/Grace/)
- [Grace batch system](https://hprc.tamu.edu/kb/User-Guides/Grace/Batch/)
- [Grace key policies](https://hprc.tamu.edu/kb/User-Guides/Grace/Policies/)

Community examples are design references, not Grace policy:
[Duke cluster assistant](https://computing.cs.duke.edu/software/ai/),
[Setty Lab HPC skills](https://github.com/settylab/fh-hpc-skills), and
[SciMate orchestration](https://github.com/SciMate-AI/HPC-Skills/tree/main/skills/hpc-orchestration).
