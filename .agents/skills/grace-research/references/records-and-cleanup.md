# Records, repository integration, and cleanup

## One run record

Keep reusable instructions in this skill and mutable research state in the project.
Reuse an existing run manifest or ledger before creating another. Each run needs
identity, purpose, input identities/checksums, code commit plus dirty-code hashes
if applicable, settings, model/pseudopotential identity, seeds, environment,
expected count, job/attempt IDs, output locations, checks and exclusions. Record
who/what verified the evidence and when. Do not store numerical results as timeless
facts in the skill.

## GitHub linkage

The confirmed calculations/workflow repository is
[Shiba9908/grace](https://github.com/Shiba9908/grace), supplied by Shib on
2026-10-29. Its local checkout is `~/E Drive/mace-grace-setup/repository`.
The canonical skill is tracked there at `.agents/skills/grace-research/`.
The older local `agent-skills/grace-research` location is a compatibility symlink;
the existing Codex registration resolves through it to this checkout.

Verify the remote owner/repository and current instructions from a supplied URL,
an authenticated repository record, or `git remote -v`. Do not guess the repository
from the word "MACE" or substitute the upstream ACEsuit repository.

Prefer a canonical tracked `.agents/skills/grace-research/` in the calculations
repository, with local discovery pointing to that same folder when supported.
If repository access is unavailable, keep the local skill usable and state what
could not be synchronized. Avoid making two independently edited copies.
For a documented cross-agent setup, use a relative symlink from the appropriate
project skill directory rather than duplicating the skill text.

Inspect working-tree changes and concurrent work; use an isolated branch or
checkout when needed. Stage only task files. Do not force-push or merge unrelated
changes. Publish authorized changes as a reviewable branch/PR if direct default-
branch changes are not already the established workflow. A user request to link
the skill does not authorize uploading all local research files.

Keep code, small configs, run metadata, documentation and small representative
fixtures in Git. Keep bulk trajectories, model weights, caches and full run
directories in appropriate research storage, with manifest links/checksums.

## Cleanup with evidence

When cleanup is requested, inventory before mutation and record old path, action,
new/canonical path, reason and SHA-256 where relevant in a single cleanup manifest.
Inspect references before deleting or moving a referenced path. Preserve unique
source, raw data, provenance, collaborator attribution, configurations and final
deliverables. Different force tolerances, seeds or protocols can produce identical
bytes while remaining distinct scientific records.

- Remove confirmed redundant downloads or superseded generated copies only after
  retaining and verifying a canonical copy and repairing references as needed.
- Do not deduplicate empty `__init__.py` files, package resources or runtime files
  by content hash. Do not delete scientific records simply because they are old,
  failed, inconvenient, or not part of the current result.
- Archive unique historical reviews/prompts/snapshots outside the active work area
  while keeping their provenance. Mark them historical rather than executable
  current guidance. Do not treat archiving as storage reclamation.
- Prefer a few purpose-based folders: motifs, methods, structures, reports, and
  archive. Create a method folder when it has actual content; do not generate an
  empty directory tree for every future possibility.
- For a deletion batch, recheck file identity immediately before acting, retain
  a recoverable backup outside the active tree when warranted, and verify the
  retained copy afterward. Do not delete remote Grace data as a side effect of
  local E Drive cleanup.

Do not create a new status note for every check. Update the existing project index
and run record; keep operational logs separate from scientific results.

Design reference:
[JCLiuGroup research records](https://github.com/JCLiuGroup/AI-Computational-Chemist#research-orchestration-layer).
