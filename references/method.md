# Modularization method

## The common spine

Apply these rules in every mode unless the mode explicitly omits a probe.

1. **Census before carving.** Build a bounded inventory with stable item identities and evidence. The inventory, not the proposed tree, is the coverage denominator.
2. **Carve at joints.** Three to seven children is the default legibility band, not a target. One child collapses; two require a genuine dichotomy; more than seven requires evidence that another grouping layer would misrepresent the domain.
3. **Distinguish decompositions from populations.** A decomposition has differentiated parts whose relations help constitute the whole. A population is an extensible set of peers. Keep a population flat and expose useful facets.
4. **Keep trivial peer tails in a gloss.** Do not promote a long list of structurally identical members into tree nodes merely because they exist.
5. **Let depth vary by branch.** Descend until the requested resolution reaches atomic capabilities or positive semantic kinds. Do not force a balanced tree.
6. **Prefilter decorations before generation.** Status, constraint, provenance, audit, aspiration, lifecycle, and presentation material attach to substantive nodes or Residuals. If decorations enter candidate generation, every candidate inherits the same junk drawer.
7. **Require a positive kind.** A node earns a slot because its constituents cohere on their own terms, not because they are excluded from other nodes.
8. **Home every constituent once.** Give each constituent one primary leaf home. Preserve meaningful alternate homes and overlaps through typed residual relations rather than duplicate membership.
9. **Generate paradigms before granularities.** First compare organizing principles at their natural child counts. Only after selecting the strongest principle compare native cuts at nearby N values.
10. **Generate every N natively.** Do not produce N=4 by merging an N=5 cut. A native four-way carve can reveal a boundary the five-way carve never represented.
11. **Use one ply of lookahead.** Sketch likely children before locking a parent. Repeated child-level crossings expose a bad parent boundary.
12. **Lock one layer before descending.** A bad root contaminates every lower level.
13. **Probe kind-homogeneity.** State the positive kind shared by each sibling set and inspect the weakest-cohering sibling.
14. **Separate contract validity from semantic review.** Deterministic validation establishes schema, referential integrity, coverage, and lineage arithmetic. Candidate comparison and semantic fitness remain evidence-backed judgment.
15. **Residualize every defensible recut.** Record seam-straddlers, alternate homes, low-confidence cuts, topology warnings, shape mismatches, and unresolved items.

## Light mode

Use the common spine through one-layer generation, but omit the paradigm sweep, native N-array, one-ply lookahead, and kind-homogeneity probe. Preserve census accounting, relations, Residuals, and the population sanity check. Set `semantic_review.status` to `provisional`; omitted checks remain `not_run` with a claim explaining the omission.

## Medium mode

Generate at least two genuinely distinct candidate cuts when the material admits them. Compare them semantically rather than by child count. Run population sanity, one-ply lookahead, and kind-homogeneity. Mark semantic review `reviewed` only when each required check is `passed` or `flagged`, states a falsifiable claim, and points to evidence; a flagged result must also appear in Residuals.

## Heavy mode

### 1. Paradigm sweep

Generate one blind sketch for every plausible organizing principle at its natural N. Candidate principles include capability, information ownership, transformation stage, object kind, lifecycle, stakeholder, and dependency seam. Compare referent stability, mass distribution, self-understanding, coupling, source-model crossings, and residual burden.

### 2. Native N-array

Within the winning principle, independently generate plausible cuts inside the three-to-seven band. If every N is poor, reconsider the organizing principle rather than choosing the least bad count.

### 3. One-ply lookahead

Sketch one child layer for every candidate parent. Prefer the cut whose children inherit cleanly and whose inventory relations cross fewer sibling boundaries.

### 4. Adversarial probe

For every locked sibling set, state the shared positive kind, identify the weakest sibling, test whether its contents split into different kinds, quarry repairs from losing cuts, and residualize every unresolved judgment.

### 5. Layer lock

Lock the current layer only after population sanity, lookahead, homogeneity, and census accounting complete. Then recurse independently.

## Reconciliation and resynthesis

Reconciliation takes the prior canonical artifact as evidence, never as authority.

1. Rebuild the current inventory from source and reconcile item identities before considering the old tree.
2. Locate the lowest incumbent layer containing all changed, added, retired, or newly crossing constituents.
3. Generate at least one fresh challenger at that layer without deriving it by editing the incumbent.
4. Compare incumbent and challenger on positive kind, coupling, relation crossings, residual burden, and child-level inheritance.
5. Choose **local reconciliation** when the incumbent root organizing principle still wins and instability remains inside named branches.
6. Choose **global resynthesis** when a competing root principle materially improves the carve, the root kind fails, or change crosses several top-level boundaries such that local repairs preserve the wrong ontology.
7. Preserve stable node IDs for unchanged referents. Mint new IDs for new referents, retire removed IDs, and record the exact preserved/added/retired sets in lineage.

File-change volume may trigger inspection, but it cannot decide local versus global resynthesis. The decision follows semantic and relational drift.

## Stable identity

Use opaque namespaced UUIDs for artifact, item, node, and relation identity. Keep labels, filesystem paths, and display ordinals as mutable attributes. During reconciliation, identity follows the continuing referent: a renamed module keeps its ID; a split retires the original only when no single successor preserves its identity; a merge records the retired inputs and mints a new referent unless one input clearly subsumes the others.

## Stopping rule

Stop descending when one of these holds:

- the node is one capability, concern, or semantic kind at the caller's needed resolution;
- further children would be trivial peers better kept in a gloss or facet;
- evidence cannot support a defensible finer cut, which becomes a low-confidence residual;
- the structure is intrinsically overlapping, which becomes an explicit relation or semi-lattice signal.
