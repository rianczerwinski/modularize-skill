# Canonical output contract — schema version 2

The canonical artifact is one JSON object. Schema version 2 is intentionally incompatible with version 1; see [migration-v1-v2.md](migration-v1-v2.md).

```json
{
  "schema_version": 2,
  "artifact_id": "carve:<uuid>",
  "subject": "bounded subject",
  "operation": "initial | reconcile",
  "mode": "light | medium | heavy",
  "requested_shape": "decomposition | population",
  "diagnosed_shape": "decomposition | population",
  "organizing_principle": "positive basis, or null for a population",
  "caller_constraints": [],
  "inventory": [],
  "relations": [],
  "lineage": {},
  "tree": {},
  "semantic_review": {},
  "residuals": {}
}
```

## Identity contract

All durable identities are opaque, namespaced UUIDs:

- artifact: `carve:<uuid>`;
- inventory item: `item:<uuid>`;
- node: `node:<uuid>`;
- relation: `relation:<uuid>`.

Labels, filesystem paths, and display ordinals are attributes, not identity. Reconciliation preserves IDs for continuing referents and records additions and retirements mechanically.

## Inventory contract

Every inventory row has:

```json
{
  "id": "item:<uuid>",
  "label": "concise referent",
  "role": "constituent | decoration",
  "evidence": [{"ref": "resolving artifact or caller statement", "note": "why it establishes membership"}]
}
```

The inventory must be non-empty. A constituent appears exactly once in one leaf's `member_ids` or exactly once in `residuals.unresolved_items`. A decoration appears exactly once in `residuals.excluded_decorations`. Duplicate primary homes are invalid; alternate homes belong in `seam_straddlers` or `semi_lattice_signals`.

## Node contract

Every node has:

```json
{
  "id": "node:<uuid>",
  "label": "positive name",
  "kind": "positive semantic kind shared by siblings",
  "gloss": "what this node contains",
  "cohesion_basis": "why these contents belong together",
  "member_ids": [],
  "children": [],
  "facets": []
}
```

Internal nodes have children and no direct members. Leaves home inventory constituents. A population remains a single root leaf with non-empty facets and its peer members in `member_ids`.

One-child layers are invalid. Two-child layers add `dichotomy_reason`. Three to seven children need no numerical justification. A node with more than seven children adds:

```json
"fanout_exception": {
  "reason": "why these are genuinely one irreducible sibling set",
  "rejected_grouping": "the grouping layer considered and why it would falsify the domain"
}
```

For medium and heavy outputs, siblings declare one shared `kind`. The field is an auditable claim; semantic review supplies the evidence.

## Relation contract

Non-tree evidence is explicit:

```json
{
  "id": "relation:<uuid>",
  "kind": "dependency | interaction | overlap",
  "source_id": "item:<uuid> | node:<uuid>",
  "target_id": "item:<uuid> | node:<uuid>",
  "reason": "why the relation matters to the carve",
  "evidence": [{"ref": "resolving artifact", "note": "observed relation"}]
}
```

Relations do not create additional primary homes. Their endpoints must resolve inside the artifact.

## Lineage contract

```json
{
  "parent_artifact_id": null,
  "reconciliation_scope": "initial | local | global",
  "decision": "why this scope follows from the incumbent challenge",
  "preserved_node_ids": [],
  "added_node_ids": [],
  "retired_node_ids": []
}
```

An initial carve uses `parent_artifact_id: null`, `reconciliation_scope: initial`, no preserved or retired IDs, and lists every current node under `added_node_ids`. A reconciliation names its parent, uses local or global scope, and partitions parent/current identities into exact preserved, added, and retired sets. Run the validator with `--parent` so those claims are checked against the prior artifact.

## Semantic-review contract

Semantic review deliberately avoids the word `verified`:

```json
{
  "status": "provisional | reviewed",
  "checks": {
    "population_sanity": {"status": "not_run | passed | flagged", "claim": "", "evidence": []},
    "paradigm_sweep": {"status": "not_run | passed | flagged", "claim": "", "evidence": []},
    "native_n_array": {"status": "not_run | passed | flagged", "claim": "", "evidence": []},
    "one_ply_lookahead": {"status": "not_run | passed | flagged", "claim": "", "evidence": []},
    "kind_homogeneity": {"status": "not_run | passed | flagged", "claim": "", "evidence": []},
    "incumbent_challenge": {"status": "not_run | passed | flagged", "claim": "", "evidence": []}
  }
}
```

Light remains provisional. Medium requires population sanity, lookahead, and homogeneity. Heavy additionally requires the paradigm sweep and native N-array. Reconciliation in medium or heavy also requires the incumbent challenge. Every passed or flagged check states its claim and points to evidence. `flagged` means unresolved matter is represented in Residuals.

The validator proves structural assertions and accounting. `semantic_review` records judgment procedure and evidence; it is not converted into deterministic truth by living inside valid JSON.

## Residual contract

All seven arrays are mandatory:

- `excluded_decorations`: `{"item_id": "item:<uuid>", "distributed_as": "...", "evidence": [...]}`;
- `unresolved_items`: `{"item_id": "item:<uuid>", "reason": "...", "next_evidence": "..."}`;
- `seam_straddlers`: `{"item_id": "item:<uuid>", "home_node_id": "node:<uuid>", "alternate_node_ids": ["node:<uuid>"], "reason": "..."}`;
- `judgment_calls`: `{"decision": "...", "alternative": "...", "reason": "...", "node_ids": ["node:<uuid>"]}`;
- `low_confidence`: `{"node_id": "node:<uuid>", "reason": "..."}`;
- `semi_lattice_signals`: `{"item_ids": ["item:<uuid>"], "node_ids": ["node:<uuid>"], "reason": "..."}`;
- `population_warnings`: `{"item_id": "item:<uuid> | null", "reason": "..."}`.

Every referenced item and node must exist. A seam-straddler's `home_node_id` must be the item's actual primary leaf home. A requested/diagnosed shape mismatch requires a flagged population-sanity check and at least one population warning.

## Mechanical validation

Run:

```text
python3 scripts/validate.py result.json
python3 scripts/validate.py result-v2.json --parent previous-v2.json
python3 scripts/validate.py result.json --receipt result.validation.json
```

The optional receipt records the artifact hash, schema version, and validator version. A reconciliation receipt also binds the supplied parent artifact's identity and hash. Consumers should rerun validation or verify every recorded hash before trusting a stored receipt. Parent binding proves which bytes were compared; it does not recursively re-prove the parent's own lineage.
