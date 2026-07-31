---
name: modularize
description: Decompose a body of material into a coherent, auditable module tree with light, medium, or heavy semantic carving. Use when the user asks to modularize, decompose, carve, factor, structure, or find the natural joints in a workframe, system, ontology, roadmap, document, inventory, or conceptual field; when a hierarchy has junk-drawer or cross-cutting buckets; or when another skill needs a reusable decomposition service. Distinguishes decompositions from populations, preserves overlaps as residuals, and emits canonical JSON with an optional derived Markdown view.
---

# modularize

Turn a bounded body of material into a coherent module tree. Optimize for positive semantic kinds, strong within-module cohesion, weak between-module coupling, and explicit uncertainty.

## Inputs

Establish these before carving:

- **subject** — the bounded material to organize;
- **requested shape** — caller-declared `decomposition` or `population`;
- **mode** — `light`, `medium`, or `heavy`;
- **inventory** — the actual items, evidence, or concepts in scope;
- **caller constraints** — stable names, downstream schema needs, forbidden moves, or required coverage.

If the caller omits the requested shape, infer their intent from the verb they used, record that inference, and still run the population sanity check. Do not silently replace a requested decomposition with a population or the reverse.

## Choose effort by observable conditions

- **Light** — use for a provisional, low-stakes cut when the joints are obvious or the caller explicitly asks for speed. Produce one carve, run the population sanity check, keep Residuals, skip the adversarial probes, and mark the result `unverified`.
- **Medium** — default when the material has partial self-description or more than one plausible cut but no live dispute. Compare the plausible cuts, use one ply of lookahead, run the kind-homogeneity probe, and mark the result `verified` only after both pass.
- **Heavy** — use when joints are contested, self-description is absent or misleading, downstream use is load-bearing, or a prior carve failed. Run the full paradigm sweep, native N-array, one-ply lookahead, and adversarial probes.

Read [references/method.md](references/method.md) for the complete heavy procedure and the precise medium/light omissions.

## Procedure

1. **Bound and inventory.** State what is in scope, what evidence supports membership, and what the caller has fixed.
2. **Prefilter decorations.** Remove status, provenance, constraints, audits, aspirations, presentation modes, and other material that describes a constituent rather than constituting one. Preserve each as metadata or a residual; never lose it.
3. **Sanity-check the requested shape.** A decomposition contains differentiated functional or semantic parts. A population contains peer members of an extensible set and wants facets, not forced buckets. Flag a mismatch; do not silently change the caller's declaration.
4. **Carve one layer.** Follow the selected mode. Treat 3–7 children as a diagnostic band, not a target. Never derive lower-N candidates by merging a higher-N cut.
5. **Stress the cut.** In medium and heavy modes, inspect each sibling set for one positive kind and use one ply of child-level lookahead to expose unstable parents. Repair with distinctions found in losing candidates.
6. **Descend only after the layer locks.** Reapply the same procedure independently inside each non-atomic node. Stop when a node expresses one capability, concern, or positive semantic kind at the resolution the caller needs.
7. **Residualize overlap and judgment.** Home seam-straddlers by substance, record plausible alternate homes, and flag semi-lattice structure rather than emitting a DAG.
8. **Emit canonical JSON.** Follow [references/contract.md](references/contract.md). Produce Markdown only as a derived view of that JSON.
9. **Validate file-backed output.** Run `python3 scripts/validate.py <result.json>`. A validator pass proves conformance to the contract, not semantic correctness.

## Quality tests

A locked decomposition must satisfy:

- **coverage** — every in-scope constituent is homed or named in Residuals;
- **positive kind** — siblings answer “what are these?” with the same positive kind, not merely “things not elsewhere”;
- **cohesion** — each node has a single intelligible basis;
- **coupling** — moving one concern should disturb as few sibling modules as possible;
- **level consistency** — siblings occupy the same analytical level;
- **stable lookahead** — a plausible child layer fits the parent without repeatedly crossing sibling boundaries;
- **honest topology** — load-bearing overlaps are recorded as semi-lattice signals;
- **population integrity** — peer populations remain facet-navigable rather than bucketed into a fake taxonomy.

## Output

The JSON object is canonical. It carries the tree, declared and diagnosed shapes, effort mode, verification record, and mandatory Residuals arrays. Use the schema and field meanings in [references/contract.md](references/contract.md).

When the user wants a human-facing answer, render a compact Markdown tree followed by Residuals, but retain the JSON as the machine-consumable source whenever another skill or tool will consume the result.

## Prior-art posture

This skill composes established modularity criteria rather than claiming to invent them: Constantine–Myers–Stevens cohesion, Parnas information hiding, Simon near-decomposability, Alexander's hierarchical decomposition and semi-lattice warning, Design Structure Matrices, and grounded-theory coding. Its distinct contribution is the agent-operable combination of graded effort, decoration prefiltering, paradigm-versus-granularity separation, adversarial kind checks, and mandatory residuals. See [references/lineage.md](references/lineage.md).

## Revisit when

- A real corpus loses load-bearing meaning under a tree: add a canonical semi-lattice representation.
- Human review becomes the majority consumption path: reconsider Markdown as canonical.
- Medium still means only “between light and heavy” after three real uses: collapse to two modes.
- A light result is consumed as final despite its status: remove light or require the kind probe.
- Caller shape declarations are wrong more than roughly one time in five: consider automatic shape selection.
- A modularize revision breaks a dependent skill's expected shape: consider a shared versioned contract rather than procedural dependency.

## Anti-patterns

Read [antipatterns.md](antipatterns.md) before a heavy carve or when repairing a failed hierarchy.
