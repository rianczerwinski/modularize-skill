# Anti-patterns

### Tree-defined coverage

❌ Wrong: List only the items that fit the proposed tree, then report that every listed item has a home.

✅ Right: Build the evidence-bearing inventory before carving and require every item to appear exactly once in a leaf or typed Residual.

Why it flips: A tree cannot prove it covered material it silently omitted; an independent inventory supplies the denominator.

Prevents: A clean-looking carve whose missing constituents are invisible.

### Semantic verification by contract validation

❌ Wrong: Set `status: verified` because the JSON has every required field and the validator exits zero.

✅ Right: Call the artifact contract-valid after the validator passes and call its semantics provisional or reviewed according to the evidence-bearing judgment procedure.

Why it flips: Deterministic validation can establish structure, references, and accounting, not whether the chosen ontology best fits the material.

Prevents: Machine authority laundering a self-authored semantic judgment.

### Positional identity

❌ Wrong: Treat `1.2.3` or `packages/web` as the node's durable identity.

✅ Right: Preserve an opaque `node:<uuid>` across reconciliation and derive display ordinals and paths from the current view.

Why it flips: Reordering and relocation change position without changing the referent.

Prevents: Every local recarve looking like wholesale deletion and recreation.

### Patching the incumbent without a challenger

❌ Wrong: Move newly awkward items between existing modules until the old tree looks tolerable again.

✅ Right: Generate a fresh candidate at the lowest affected layer and compare it against the incumbent before choosing local reconciliation or global resynthesis.

Why it flips: Patching assumes the old ontology remains correct; a challenger makes that assumption falsifiable.

Prevents: Ontological drift being absorbed as endless exceptions.

### Change-count resynthesis

❌ Wrong: Rebuild the entire tree whenever thirty percent of files changed, or preserve it whenever the diff is smaller.

✅ Right: Use file churn only to locate pressure, then decide from positive-kind failure, relation crossings, coupling, residual burden, and whether a competing root principle wins.

Why it flips: Mechanical churn and semantic drift are correlated imperfectly.

Prevents: Cosmetic refactors causing ontology churn and small foundational changes being missed.

### Treating the band as a quota

❌ Wrong: “There must be five modules, so split the largest category until there are five.”

✅ Right: Carve at semantic joints, then read one, two, or more than seven children as diagnostic evidence requiring collapse, a dichotomy reason, or a fan-out exception.

Why it flips: Child count evaluates a cut; it does not generate the cut.

Prevents: Numerically tidy but semantically arbitrary hierarchies.

### Fan-out exception as a waiver word

❌ Wrong: Add `fanout_exception: {"reason": "eight seemed natural"}` and keep eight siblings.

✅ Right: Name the grouping layer considered and demonstrate why it would falsify the positive kind or relations among the irreducible siblings.

Why it flips: The exception must contain the failed alternative, not merely restate preference.

Prevents: The default maximum disappearing behind boilerplate.

### Split-derived candidates

❌ Wrong: Generate N=6 once, then merge siblings to obtain N=5, N=4, and N=3.

✅ Right: Generate each plausible N independently inside the winning organizing principle.

Why it flips: Native generation can reveal boundaries absent from the higher-N cut.

Prevents: A fake search space whose candidates inherit one initial mistake.

### Decorations become modules

❌ Wrong: Put Roadmap, Constraints, Research, and Audits beside the system's substantive parts.

✅ Right: Inventory them as decorations and distribute them as state, provenance, evidence, constraints, or Residuals on substantive nodes.

Why it flips: Decorations describe constituents; they are not constituents of the same kind.

Prevents: The same junk drawer contaminating every candidate carve.

### “Cross-cutting” as a positive kind

❌ Wrong: Create Shared, Cross-cutting, or Miscellaneous for everything that does not fit elsewhere.

✅ Right: Home each item once by substance and represent genuine alternate homes through node-referenced seam or semi-lattice records.

Why it flips: Non-membership in other nodes is coincidental cohesion, not module identity.

Prevents: Residual buckets disguised as architecture.

### Bucketing a population

❌ Wrong: Force customers, works, people, cases, or runs into a permanent three-to-seven branch taxonomy.

✅ Right: Keep the peer set in one population leaf and expose facets such as type, date, owner, state, or provenance.

Why it flips: Populations extend by adding members; decompositions explain differentiated parts.

Prevents: Arbitrary categories that break as the population grows.

### One-shot root-to-leaf generation

❌ Wrong: Produce the complete hierarchy in one pass and judge only the final appearance.

✅ Right: Lock one layer after candidate comparison and stress tests, then recurse independently.

Why it flips: A bad parent cut otherwise propagates into every descendant.

Prevents: Deeply polished trees built on an unstable root.

### Silent overlap loss

❌ Wrong: Choose one home for an item that materially belongs to several modules and erase the other relations.

✅ Right: Choose one primary home and record every load-bearing alternate through typed node references.

Why it flips: Serialization may be a tree even when reality is a semi-lattice.

Prevents: False exclusivity and invisible information loss.

### Light output masquerades as final

❌ Wrong: Skip the adversarial probes and still mark semantic review `reviewed`.

✅ Right: Keep light output `provisional`; rerun in medium or heavy before load-bearing consumption.

Why it flips: Speed is purchased by omitting semantic evidence, so the status must expose that omission.

Prevents: Provisional cuts accumulating authority they never earned.

### Evidence-free review labels

❌ Wrong: Write `kind_homogeneity: passed` with no claim or inspection trace.

✅ Right: Name the shared positive kind, identify the weakest sibling, and point the check to the candidate comparison or residual record.

Why it flips: A status word is not evidence that the check ran.

Prevents: Procedural theater.

### Derived-view drift

❌ Wrong: Maintain a human Markdown tree separately from the canonical JSON.

✅ Right: Regenerate every human view from the validated JSON artifact.

Why it flips: One source prevents human and machine representations from silently diverging.

Prevents: Dependent skills consuming a different carve from the one a person reviewed.
