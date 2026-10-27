---
name: modularize
description: Decompose or reconcile a bounded body of material into a coherent, auditable module structure with light, medium, or heavy semantic carving. Use when the user asks to modularize, decompose, carve, factor, remodularize, resynthesize, reconcile, structure, or find the natural joints in a workframe, system, ontology, roadmap, document, inventory, or conceptual field; when a hierarchy has junk-drawer or cross-cutting buckets; or when another skill needs a reusable decomposition service. Distinguishes decompositions from populations, accounts for every source constituent, preserves overlap as explicit relations and residuals, and emits canonical versioned JSON with optional derived views.
license: MIT
---

# modularize

Turn a bounded inventory into a coherent module structure. Optimize for positive semantic kinds, strong within-module cohesion, weak between-module coupling, complete source accounting, stable identity, and explicit uncertainty.

## Inputs

Establish these before carving:

- **subject** — the bounded material to organize;
- **operation** — `initial` for a new carve or `reconcile` for an existing canonical artifact;
- **requested shape** — caller-declared `decomposition` or `population`;
- **mode** — `light`, `medium`, or `heavy`;
- **inventory** — stable-ID constituents and decorations with evidence for membership;
- **relations** — known dependencies, interactions, or overlaps that should inform the cut;
- **caller constraints** — stable names, downstream schema needs, forbidden moves, or required coverage;
- **parent artifact** — mandatory for reconciliation.

If the caller omits the requested shape, infer it from their verb, record the inference, and still run the population sanity check. Preserve a requested shape that disagrees with the diagnosis and flag the mismatch rather than silently changing the request.

## Choose semantic effort by observable conditions

- **Light** — use for a provisional, low-stakes cut when the joints are obvious or the caller explicitly asks for speed. Produce one carve, run the population sanity and census-accounting checks, retain every Residual, skip the adversarial probes, and mark semantic review `provisional`.
- **Medium** — default when the material has partial self-description or more than one plausible cut but no live dispute. Compare distinct candidates, use one ply of lookahead, run the kind-homogeneity probe, and mark semantic review `reviewed` only after the required checks carry evidence.
- **Heavy** — use when joints are contested, self-description is absent or misleading, downstream use is load-bearing, or a prior carve failed. Run the full paradigm sweep, native N-array, lookahead, and adversarial probes.

Read [references/method.md](references/method.md) for the complete procedure, including reconciliation and the local-versus-global resynthesis decision.

## Procedure

1. **Bound and census.** Mint stable `item:<uuid>` identities, state what is in scope, and attach resolving evidence. The inventory is the denominator; every item must end homed or residualized.
2. **Prefilter decorations.** Classify status, provenance, constraints, audits, aspirations, and presentation modes as decorations. Distribute them as metadata or Residuals without letting them become peer modules.
3. **Sanity-check shape.** A decomposition contains differentiated parts. A population contains peer members of an extensible set and wants facets rather than buckets.
4. **Carve one layer.** Follow the selected mode. Treat three to seven children as the default legibility band, not a target. More than seven requires an explicit demonstration that another grouping layer would falsify the domain.
5. **Stress the cut.** In medium and heavy modes, inspect each sibling set for one positive kind and use one ply of child-level lookahead to expose unstable parents. Repair with distinctions found in losing candidates.
6. **Reconcile explicitly.** Challenge an incumbent carve with a fresh candidate at the lowest affected layer. Recarve locally when the incumbent organizing principle still wins; resynthesize globally when a competing root principle materially reduces crossings, coupling, or residual burden.
7. **Descend after the layer locks.** Reapply the procedure independently inside each non-atomic node. Keep stable `node:<uuid>` identities for unchanged referents across reconciliation; display ordinals are derived and disposable.
8. **Account and residualize.** Give every constituent exactly one primary leaf home or place it in `unresolved_items`. Record alternate homes, semi-lattice structure, low confidence, and judgment calls without duplicating their source facts.
9. **Emit canonical JSON.** Follow [references/contract.md](references/contract.md). Produce Markdown or diagrams only as derived views.
10. **Validate mechanically.** Run `python3 scripts/validate.py <result.json>`. For reconciliation, add `--parent <previous.json>`. A pass proves contract conformance and census accounting, not semantic correctness.

## Quality tests

A reviewed decomposition must satisfy:

- **coverage** — every inventory item is homed exactly once or named in a typed Residual;
- **positive kind** — siblings answer “what are these?” with the same positive kind;
- **cohesion** — each node has one intelligible basis;
- **coupling** — moving one concern disturbs as few siblings as possible;
- **level consistency** — siblings occupy the same analytical level;
- **stable lookahead** — plausible children fit their parent without repeated sibling crossings;
- **honest topology** — load-bearing overlaps remain explicit relations or semi-lattice signals;
- **population integrity** — peer populations remain facet-navigable;
- **identity continuity** — reconciliation preserves IDs for unchanged referents and records additions and retirements;
- **incumbent challenge** — reconciliation does not preserve the old ontology merely because it already exists.

## Output and assurance language

The versioned JSON artifact is canonical. It carries the inventory, source evidence, semantic tree, non-tree relations, lineage, semantic-review record, and mandatory Residuals. Render compact human views from that artifact rather than maintaining parallel truth.

Call the artifact **contract-valid** only after the validator passes. Call its semantics **provisional** or **reviewed** according to the recorded judgment procedure. Never use `verified` for a carve: deterministic validation can establish structure and accounting, while semantic fitness remains an evidence-backed judgment.

## Prior-art posture

This skill composes established modularity, architecture-recovery, traceability, and structural-validation methods. See [references/lineage.md](references/lineage.md) for the retrieved lineage and novelty boundary.

## Revisit when

- Explicit non-tree relations become the majority consumption path: consider a graph-first canonical form with the tree as one projection.
- Medium still means only “between light and heavy” after three real uses: collapse to two modes.
- Light output is repeatedly consumed as final: remove light or require the homogeneity probe.
- Reconciliation frequently produces disputed identity continuity: add a dedicated identity-migration tool.
- The seven-child exception is routinely invoked: the current subject may be a population or the grouping criterion may be wrong.
- A dependent skill cannot consume schema version 2: migrate that consumer rather than weakening the contract.

## Anti-patterns

Read [antipatterns.md](antipatterns.md) before a heavy carve, before reconciliation, or when repairing a failed hierarchy.

## Additional resources

- [references/contract.md](references/contract.md) — canonical schema version 2 and field semantics.
- [references/migration-v1-v2.md](references/migration-v1-v2.md) — breaking changes and consumer migration.
- [references/method.md](references/method.md) — complete mode procedures and resynthesis law.
- [references/lineage.md](references/lineage.md) — retrieved prior art and reuse posture.
- [examples/feedback-loop.json](examples/feedback-loop.json) — positive schema-version-2 example.
- [antipatterns.md](antipatterns.md) — paired wrong-to-right failure modes.
