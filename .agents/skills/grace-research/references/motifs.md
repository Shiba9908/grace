# Motifs across alloy development

## Define before enumerating

Specify the lattice/phase, host composition, central object (metal site,
interstitial, vacancy, bond, or transition state), shell geometry, species order,
symmetry action, and canonicalization version. Composition counts alone do not
identify a geometric motif. A count from one crystal, species count, or shell
definition is not universal.

Keep geometry catalogs separate from energy/property datasets. Kyryl's catalog
in the local `collaborators/kyryl` archive provides motif geometry; it is not a
DFT benchmark. Preserve its source/license and the selected symmetry convention.
Validate site vectors, shell distances/multiplicities, permutation closure and
equivalence before a large enumeration. Use an independent count or small
explicit enumeration where it can expose a symmetry mistake.

## Sampling and controlled comparisons

- Record composition, atom count, seed, random/SQS/ordered construction, initial
  motif and final motif. Do not label random structures as SQS.
- Verify that a requested fixed shell is actually fixed in the generated structure,
  that periodic images do not duplicate neighbours, and that cell composition is
  feasible after imposing the motif.
- For within-motif variation, vary the intended outer environment while holding
  the defined motif fixed. For between-motif variation, use a matched protocol.
  Record whether volume is common, per-host relaxed, or finite-temperature derived.
- Check whether relaxation changes the motif or moves H/defects to another site.
  Report retained and migrated subsets separately; do not discard migration silently.
- Group final basins using coordinates with periodic minimum-image distances and
  appropriate host alignment/identity. Energy or chemistry alone is insufficient.
- Report per-motif sample counts, exclusions, dispersion definition and weighting.
  Distinguish pooled within-motif SD from SD across motif means. Bootstrap or split
  by independent host where observations share the same host.

For H interstitial studies, T/O can describe the starting site or the final site;
label which one is meant. Retain ambiguous/intermediate labels when the geometry
does not justify a definite classification. An H-only Hessian probes a restricted
subspace and does not establish full-system dynamical stability.

## Extend without assuming validation

Use the same motif identifiers to connect structure, MLIP energies, DFT checks,
hop barriers, and coarse-grained parameters. When changing alloy chemistry,
lattice, shells, or property, reassess the symmetry and model domain. Describe
unimplemented workflows as planned. Never fill missing motif properties with
unlabelled guesses.
