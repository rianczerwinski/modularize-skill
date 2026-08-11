# Lineage and novelty boundary

## Closest methodological predecessors

- **Stevens, Myers, and Constantine, “Structured Design” (1974)** — cohesion and coupling provide the module-quality axis. Coincidental or merely logical cohesion explains residual and “cross-cutting” buckets; functional cohesion supplies the positive ideal. [DOI](https://doi.org/10.1147/sj.132.0115)
- **David Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules” (1972)** — hide design decisions likely to change; modularize by what varies together rather than surface workflow alone. [DOI](https://doi.org/10.1145/361598.361623)
- **Herbert Simon, “The Architecture of Complexity” (1962)** — near-decomposability: strong interactions within modules and weaker interactions between them. [DOI](https://doi.org/10.2307/1886091)
- **Christopher Alexander, _Notes on the Synthesis of Form_ (1964)** — hierarchical decomposition by natural cleavages in interacting requirements. “A City Is Not a Tree” (1965) supplies the corrective: many living structures are semi-lattices, so a tree must disclose load-bearing overlaps.
- **Donald Steward, “The Design Structure System” (1981)** — Design Structure Matrices expose a complete element relation space and support clustering and sequencing. MIT's current summary emphasizes mapping every element's relations, locating missing interfaces, and clustering more effective subsystems. [DOI](https://doi.org/10.1109/TSMC.1981.4308571) · [MIT overview](https://executive.mit.edu/the-design-structure-matrix.html)
- **Murphy, Notkin, and Sullivan, “Software Reflexion Models” (1995)** — map a source model into a posited high-level model, compute convergences/divergences/absences, and iteratively refine the mapping. This directly motivates an inventory independent of the proposed carve, explicit mapping, and reconciliation that challenges rather than merely patches the incumbent. [Original paper](https://www.cs.ubc.ca/~murphy/papers/rm/fse95.html) · [method](https://www.cs.ubc.ca/~murphy/software/rmtool/rms.html)
- **NASA SWE-052 bidirectional traceability** — uniquely identify referents, map them many-to-many across lifecycle levels, and detect missing or extra elements in both directions. This supports stable identities, complete membership accounting, and orphan detection without pretending relationships are one-to-one. [NASA Software Engineering Handbook](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695427/SWE-052%2B-%2BBidirectional%2BTraceability)
- **JSON Schema validation** — separates structural assertions from annotations and defines validity as satisfaction of declared structural constraints. This supports calling the deterministic result contract-valid while keeping semantic review as an evidence-bearing judgment. [Official specification](https://github.com/json-schema-org/json-schema-spec/blob/main/specs/jsonschema-validation.md)
- **Glaser and Strauss, _The Discovery of Grounded Theory_ (1967)** — iterative coding is an adjacent multi-pass method: generate candidate categories, relate them, and consolidate around a coherent account.

## Supporting lineage

- George Miller's 1956 channel-capacity work motivates limited branching but does not justify forcing every cut to seven or treating the band as semantic truth. [DOI](https://doi.org/10.1037/h0043158)
- Baldwin and Clark's _Design Rules_ (2000) frames modules through stable interfaces and substitutability.
- Graph community detection and modularity metrics offer algorithmic alternatives when the object already has a trustworthy interaction graph; their resolution limits make them insufficient as the sole oracle for semantic corpora.

## Skill-ecosystem search

The installed canonical shelf was searched on 2026-08-10 for modularization, decomposition, stable identity, source census, semantic verification, and resynthesis. `surface` consumes modularize but does not replace its decomposition method; no installed skill supplies the same operation. A bounded public `SKILL.md` search found documentation-structure and repository-mapping skills, but no close skill combining semantic candidate generation, complete census accounting, stable identity, reconciliation, and mandatory residuals. This is evidence for revising the existing skill, not a claim that no public implementation exists.

## Reuse posture

**Resynthesize the existing skill and compose the retrieved methods.** The decomposition criteria are established prior art. The useful house-specific combination is:

- graded light, medium, and heavy semantic procedures;
- decoration prefiltering before candidate generation;
- separation of organizing-principle search from child-count search;
- one-ply semantic lookahead and kind-homogeneity probes;
- a census-backed, stable-ID canonical contract;
- explicit non-tree relations and mandatory Residuals;
- incumbent challenge with local-versus-global reconciliation;
- deterministic contract and accounting validation kept distinct from semantic review.

No new skill is warranted. `surface` remains a consumer because it adds workframe sourcing, developmental modes, regeneration, and human rendering.
