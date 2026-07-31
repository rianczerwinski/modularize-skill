# Anti-patterns

#### Treating the band as a quota
❌ Wrong: “There must be five modules, so split the largest category until there are five.”
✅ Right: Carve at semantic joints, then treat one, two, or more than seven children as diagnostic evidence to inspect.
Why it flips: Child count evaluates a cut; it does not generate the cut.
Prevents: Numerically tidy but semantically arbitrary hierarchies.

#### Split-derived candidates
❌ Wrong: Generate N=6 once, then merge siblings to obtain N=5, N=4, and N=3.
✅ Right: Generate each plausible N independently inside the winning organizing principle.
Why it flips: Native generation can reveal boundaries absent from the higher-N cut.
Prevents: A fake search space whose candidates all inherit one initial mistake.

#### Decorations become modules
❌ Wrong: Put “Roadmap,” “Constraints,” “Research,” and “Audits” beside the system's substantive parts.
✅ Right: Attach those as state, provenance, evidence, or constraints to the substantive nodes they describe.
Why it flips: Decorations describe constituents; they are not constituents of the same kind.
Prevents: The same junk drawer contaminating every candidate carve.

#### “Cross-cutting” as a positive kind
❌ Wrong: Create “Shared / Cross-cutting / Miscellaneous” for everything that does not fit elsewhere.
✅ Right: Ask what each item positively is, home it by substance, and record genuine overlaps in Residuals.
Why it flips: Non-membership in the other nodes is coincidental cohesion, not a module identity.
Prevents: Residual buckets disguised as architecture.

#### Bucketing a population
❌ Wrong: Force customers, books, people, cases, or runs into a permanent 3–7 branch taxonomy.
✅ Right: Keep the peer set as one population node and expose facets such as type, date, owner, state, or provenance.
Why it flips: Populations extend by adding members; decompositions explain differentiated parts.
Prevents: Arbitrary categories that break as the population grows.

#### One-shot root-to-leaf generation
❌ Wrong: Produce the complete hierarchy in one pass and judge only the final appearance.
✅ Right: Lock one layer after candidate comparison and stress tests, then recurse independently.
Why it flips: A bad parent cut otherwise propagates into every descendant.
Prevents: Deeply polished trees built on an unstable root.

#### Silent overlap loss
❌ Wrong: Choose one home for an item that materially belongs to several modules and erase the other relations.
✅ Right: Choose a tree home by substance and record every load-bearing alternate home under `semi_lattice_signals` or `seam_straddlers`.
Why it flips: Serialization may be a tree even when reality is a semi-lattice.
Prevents: False exclusivity and invisible information loss.

#### Light output masquerades as final
❌ Wrong: Skip the adversarial probes and still set `status` to `verified`.
✅ Right: Mark light output `unverified`; rerun in medium or heavy before load-bearing consumption.
Why it flips: Speed is purchased by omitting evidence, so the status must expose that omission.
Prevents: Provisional cuts accumulating authority they never earned.

#### Verification by label
❌ Wrong: Write `kind_homogeneity: passed` without stating a positive sibling kind or examining the weakest sibling.
✅ Right: Name the shared kind, test the weakest sibling, and residualize unresolved heterogeneity.
Why it flips: A status word is not evidence that the check ran.
Prevents: Procedural theater.

#### Markdown drift
❌ Wrong: Maintain a human Markdown tree separately from the machine JSON.
✅ Right: Treat JSON as canonical and regenerate the Markdown view from it.
Why it flips: One source prevents human and machine representations from silently diverging.
Prevents: Dependent skills consuming a different carve from the one a person reviewed.
