# Canonical output contract

Emit one JSON object with this shape:

```json
{
  "schema_version": 1,
  "subject": "bounded subject",
  "mode": "light | medium | heavy",
  "requested_shape": "decomposition | population",
  "diagnosed_shape": "decomposition | population",
  "status": "unverified | verified",
  "organizing_principle": "positive basis of the cut, or null for a population",
  "tree": {
    "id": "1",
    "label": "Subject",
    "kind": "root",
    "gloss": "what this node contains",
    "cohesion_basis": "why these contents belong together",
    "children": [],
    "facets": []
  },
  "verification": {
    "population_sanity": {"status": "passed | flagged", "note": ""},
    "paradigm_sweep": {"status": "not_run | passed | flagged", "note": ""},
    "native_n_array": {"status": "not_run | passed | flagged", "note": ""},
    "one_ply_lookahead": {"status": "not_run | passed | flagged", "note": ""},
    "kind_homogeneity": {"status": "not_run | passed | flagged", "note": ""}
  },
  "residuals": {
    "excluded_decorations": [],
    "seam_straddlers": [],
    "judgment_calls": [],
    "low_confidence": [],
    "semi_lattice_signals": [],
    "population_warnings": []
  }
}
```

## Node contract

Every node requires:

- `id` — unique within the tree;
- `label` — concise positive name;
- `kind` — the positive semantic kind shared by its siblings;
- `gloss` — what it contains;
- `cohesion_basis` — why its contents belong together;
- `children` — nested node array;
- `facets` — population navigation axes, normally empty on decomposition nodes.

For a two-child node, add `dichotomy_reason`. Do not use a one-child layer. Treat more than seven children as a failed carve that needs another grouping level.

For medium and heavy outputs, every sibling in a set must declare the same `kind`. This field is an auditable claim, not proof that the claim is semantically true; the kind-homogeneity probe supplies the judgment.

## Population contract

When `diagnosed_shape` is `population`:

- `tree.children` is empty;
- `tree.facets` is non-empty;
- `organizing_principle` is null;
- members may be summarized in `tree.gloss` or supplied by the caller outside the structural tree.

If `requested_shape` and `diagnosed_shape` differ, set `population_sanity.status` to `flagged` and add at least one `population_warnings` residual. Preserve the caller's declaration in `requested_shape`.

## Verification semantics

- Light requires `status: "unverified"`.
- Medium requires completed `one_ply_lookahead` and `kind_homogeneity`.
- Heavy requires completed `paradigm_sweep`, `native_n_array`, `one_ply_lookahead`, and `kind_homogeneity`.
- `flagged` means the check ran and its unresolved result is represented in Residuals.
- `verified` means the required procedure ran and the JSON conforms. It does not mean the carve is objectively or uniquely correct.

## Residual item shapes

Use compact objects:

- `excluded_decorations`: `{"item": "...", "distributed_as": "..."}`
- `seam_straddlers`: `{"item": "...", "home": "...", "alternate": "...", "reason": "..."}`
- `judgment_calls`: `{"decision": "...", "alternative": "...", "reason": "..."}`
- `low_confidence`: `{"item": "...", "reason": "..."}`
- `semi_lattice_signals`: `{"item": "...", "homes": ["...", "..."], "reason": "..."}`
- `population_warnings`: `{"item": "...", "reason": "..."}`

All six arrays are mandatory even when empty.
