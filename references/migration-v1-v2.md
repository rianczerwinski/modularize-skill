# Migration from schema version 1 to version 2

Schema version 2 is a breaking contract. Version 1 artifacts remain historical evidence but are not accepted by the version 2 validator.

## Field migration

| Version 1 | Version 2 | Reason |
|---|---|---|
| `status: unverified | verified` | `semantic_review.status: provisional | reviewed` | Structural validation cannot establish semantic correctness. |
| Positional node IDs such as `1.2` | Stable `node:<uuid>` IDs | Reordering and local recarving must not change referent identity. |
| Implicit input list | Required evidence-bearing `inventory` | Coverage needs a denominator independent of the produced tree. |
| Node contents implicit in prose | Leaf `member_ids` | Every constituent must be mechanically homed or residualized. |
| `verification.*.note` | `semantic_review.checks.*.{claim,evidence}` | A status word is not evidence that a judgment occurred. |
| No operation lineage | `operation` plus `lineage` | Reconciliation must distinguish preserved, added, and retired identities. |
| More than seven always rejected | More than seven requires `fanout_exception` | The band is a hard default without forcing a false grouping layer. |
| Overlap only in prose residuals | Typed item/node references and explicit relations | Consumers need referentially checkable non-tree structure. |

## Migration procedure

1. Rebuild the bounded inventory from the original source; do not infer a denominator from the old tree.
2. Mint stable artifact, item, node, and relation IDs. Preserve semantic continuity deliberately; positional IDs have no continuity value.
3. Map every constituent to one leaf or `unresolved_items`; map every decoration to `excluded_decorations`.
4. Convert old verification notes into claims plus evidence. Leave a check `not_run` when evidence that it ran cannot be recovered.
5. Treat the migrated artifact as `operation: initial` unless an actual prior version-2 parent exists. Migration from version 1 does not fabricate version-2 lineage.
6. Run `python3 scripts/validate.py <artifact.json>` and retain the failure output until every accounting or reference error is resolved.

## Consumer migration

Consumers must explicitly accept `schema_version: 2`; silently accepting both shapes invites partial parsing. Surface is the principal dependent consumer: it must persist the version-2 tree, inventory, identity, relations, semantic review, and Residuals rather than extracting only labels and children.

Do not weaken modularize version 2 to preserve a consumer's version-1 assumption. Migrate the consumer or pin it to a historical artifact until migration occurs.
