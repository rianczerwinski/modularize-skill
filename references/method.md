# Modularization method

## The common spine

Apply these rules in every mode unless the mode explicitly omits a probe.

1. **Carve at joints.** The 3–7 band is a legibility diagnostic, not a target. More than seven usually signals a missing grouping layer; one child means the layer should collapse; two children require a genuine dichotomy and an explicit reason.
2. **Distinguish decompositions from populations.** A decomposition has differentiated parts whose relations help constitute the whole. A population is an extensible set of peers. Keep a population flat and expose useful facets.
3. **Keep trivial peer tails in a gloss.** Do not promote a long list of structurally identical members into tree nodes merely because they exist.
4. **Let depth vary by branch.** Descend until the requested resolution reaches atomic capabilities or positive semantic kinds. Do not force a balanced tree.
5. **Prefilter decorations before generation.** Status, constraint, provenance, audit, aspiration, lifecycle, and presentation material attach to substantive nodes or Residuals. If decorations enter candidate generation, every candidate inherits the same junk drawer.
6. **Require a positive kind.** A node earns a slot because its constituents cohere on their own terms, not because they are excluded from the other nodes. “Cross-cutting,” “miscellaneous,” “shared,” and “meta” describe a residual relation, not a semantic kind.
7. **Home seam-straddlers by substance.** Runtime location, folder placement, or current ownership is evidence, not essence. Record alternate plausible homes in Residuals.
8. **Generate paradigms before granularities.** First compare organizing principles at their natural child counts. Only after selecting the best principle compare native cuts at nearby N values.
9. **Generate every N natively.** Do not produce N=4 by merging an N=5 cut. A native four-way carve can reveal a boundary the five-way carve never represented.
10. **Use one ply of lookahead.** Sketch likely children before locking a parent. Repeated child-level crossings expose a bad parent boundary.
11. **Lock one layer before descending.** Never generate an entire hierarchy in one pass. A bad root contaminates every lower level.
12. **Probe kind-homogeneity.** Ask of each sibling set: “What positive kind are all of these?” Constantine's cohesion scale supplies the diagnostic: coincidental and merely logical grouping are weak; functional or otherwise single-purpose cohesion is strong.
13. **Residualize every judgment that could reasonably be recut.** The output is incomplete without seam-straddlers, alternate homes, low-confidence cuts, topology warnings, and shape mismatches.

## Light mode

Use the common spine through one-layer generation, but omit the paradigm sweep, native N-array, one-ply lookahead, and kind-homogeneity probe. Preserve Residuals and the population sanity check. Set:

- `status: "unverified"`
- omitted verification checks to `not_run`

Light is a provisional hypothesis, not a final hierarchy.

## Medium mode

Use the common spine. Generate at least two genuinely distinct candidate cuts when the material admits them; compare them semantically rather than by child count. Run:

- population sanity;
- one-ply lookahead;
- kind-homogeneity.

The full paradigm sweep and native N-array may remain `not_run`. Mark `verified` only when the required probes are `passed` or `flagged` with their unresolved matter captured in Residuals.

## Heavy mode

### 1. Paradigm sweep

Generate one blind sketch for every plausible organizing principle at its natural N. Examples of principles include capability, information ownership, transformation stage, object kind, lifecycle, stakeholder, or dependency seam. Do not force each paradigm to the same N.

Compare:

- referent stability — do labels point to coherent things?
- mass distribution — does one node swallow most of the subject?
- self-understanding — does the cut match how the material actually behaves?
- coupling — do changes remain local?
- residual burden — how much load-bearing material straddles nodes?

Select the strongest principle before exploring granularity.

### 2. Native N-array

Within the winning principle, independently generate plausible cuts at nearby N values in the 3–7 diagnostic band. Compare semantic quality, not numerical tidiness. If every N is poor, reconsider the organizing principle rather than choosing the least bad count.

### 3. One-ply lookahead

Sketch one child layer for every candidate parent. Prefer the cut whose children inherit cleanly. Penalize a parent whose likely children repeatedly need siblings' contents.

### 4. Adversarial probe

For every locked sibling set:

- state the shared positive kind in a short noun phrase;
- identify the weakest-cohering sibling;
- test whether its contents split into different positive kinds;
- quarry repairs from losing cuts;
- move seam-straddlers by substance and record the judgment.

### 5. Layer lock

Lock the current layer only after the population sanity, lookahead, and homogeneity checks are complete. Then recurse independently.

## Stopping rule

Stop descending when one of these holds:

- the node is one capability, concern, or semantic kind at the caller's needed resolution;
- further children would be trivial peers better kept in a gloss or facet;
- evidence cannot support a defensible finer cut, which becomes a low-confidence residual;
- the structure is intrinsically overlapping, which becomes a semi-lattice signal.
