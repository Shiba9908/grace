# Grace alloy research

Use `.agents/skills/grace-research/SKILL.md` for this project's research workflows.
Load only the relevant method reference. Keep reusable instructions in the skill
and current run state/results in the project's run records.

This repository starts with instructions and a record checker, not a full solver
stack. Do not describe planned methods as implemented or reproduce dated local
results as newly verified evidence. Preserve existing user changes and inspect
concurrent Grace work before modifying calculation inputs.

Use Slurm for substantial computation on Grace. Do not submit jobs, cancel runs,
transfer bulk data or publish results beyond the user's requested scope.

For changes to the bundled checker, run its synthetic unittest suite from the
README. The tests require no GPU, network or scientific packages. For scientific
code added later, verify the relevant physical/numerical invariants rather than
treating scheduler completion as validation.

Keep private credentials, licensed potentials and bulk calculation outputs out of
Git. Do not send email or Slack messages. Follow Shib's shared-memory/handoff
instructions when running in their personal environment.
