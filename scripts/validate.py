#!/usr/bin/env python3
"""Validate a modularize schema-version-2 artifact and its coverage claims."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 2
VALIDATOR_VERSION = "2.0.0"
MODES = {"light", "medium", "heavy"}
OPERATIONS = {"initial", "reconcile"}
SHAPES = {"decomposition", "population"}
ITEM_ROLES = {"constituent", "decoration"}
RELATION_KINDS = {"dependency", "interaction", "overlap"}
CHECK_STATUSES = {"not_run", "passed", "flagged"}
REQUIRED_CHECKS = {
    "population_sanity",
    "paradigm_sweep",
    "native_n_array",
    "one_ply_lookahead",
    "kind_homogeneity",
    "incumbent_challenge",
}
REQUIRED_RESIDUALS = {
    "excluded_decorations",
    "unresolved_items",
    "seam_straddlers",
    "judgment_calls",
    "low_confidence",
    "semi_lattice_signals",
    "population_warnings",
}
TOP_LEVEL_KEYS = {
    "schema_version",
    "artifact_id",
    "subject",
    "operation",
    "mode",
    "requested_shape",
    "diagnosed_shape",
    "organizing_principle",
    "caller_constraints",
    "inventory",
    "relations",
    "lineage",
    "tree",
    "semantic_review",
    "residuals",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _check_keys(
    value: Any,
    required: set[str],
    optional: set[str],
    path: str,
    errors: list[str],
) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{path}: expected an object")
        return False
    for key in sorted(required - value.keys()):
        errors.append(f"{path}.{key}: missing required field")
    for key in sorted(value.keys() - required - optional):
        errors.append(f"{path}.{key}: unknown field")
    return True


def _valid_namespaced_uuid(value: Any, prefix: str) -> bool:
    if not isinstance(value, str) or not value.startswith(prefix):
        return False
    raw = value[len(prefix) :]
    try:
        parsed = uuid.UUID(raw)
    except (ValueError, AttributeError):
        return False
    return str(parsed) == raw.lower()


def _require_id(
    value: Any, prefix: str, path: str, errors: list[str]
) -> str | None:
    if not _valid_namespaced_uuid(value, prefix):
        errors.append(f"{path}: expected {prefix}<canonical-uuid>")
        return None
    return value


def _validate_string_list(
    value: Any,
    path: str,
    errors: list[str],
    *,
    nonempty: bool = False,
) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{path}: expected an array")
        return []
    if nonempty and not value:
        errors.append(f"{path}: expected a non-empty array")
    result: list[str] = []
    for index, item in enumerate(value):
        if not _nonempty_string(item):
            errors.append(f"{path}[{index}]: expected a non-empty string")
        else:
            result.append(item)
    return result


def _validate_evidence(value: Any, path: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{path}: expected a non-empty evidence array")
        return
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not _check_keys(item, {"ref", "note"}, set(), item_path, errors):
            continue
        if not _nonempty_string(item.get("ref")):
            errors.append(f"{item_path}.ref: expected a non-empty string")
        if not isinstance(item.get("note"), str):
            errors.append(f"{item_path}.note: expected a string")


def _collect_tree_ids(tree: Any) -> set[str]:
    ids: set[str] = set()
    if not isinstance(tree, dict):
        return ids
    node_id = tree.get("id")
    if isinstance(node_id, str):
        ids.add(node_id)
    children = tree.get("children")
    if isinstance(children, list):
        for child in children:
            ids.update(_collect_tree_ids(child))
    return ids


def validate_document(
    document: Any, parent_document: Any | None = None
) -> list[str]:
    errors: list[str] = []

    if not _check_keys(document, TOP_LEVEL_KEYS, set(), "$", errors):
        return errors

    if document.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"$.schema_version: expected {SCHEMA_VERSION}")

    _require_id(document.get("artifact_id"), "carve:", "$.artifact_id", errors)
    if not _nonempty_string(document.get("subject")):
        errors.append("$.subject: expected a non-empty string")

    operation = document.get("operation")
    if operation not in OPERATIONS:
        errors.append(f"$.operation: expected one of {sorted(OPERATIONS)}")

    mode = document.get("mode")
    if mode not in MODES:
        errors.append(f"$.mode: expected one of {sorted(MODES)}")

    requested_shape = document.get("requested_shape")
    diagnosed_shape = document.get("diagnosed_shape")
    if requested_shape not in SHAPES:
        errors.append(f"$.requested_shape: expected one of {sorted(SHAPES)}")
    if diagnosed_shape not in SHAPES:
        errors.append(f"$.diagnosed_shape: expected one of {sorted(SHAPES)}")

    caller_constraints = document.get("caller_constraints")
    _validate_string_list(caller_constraints, "$.caller_constraints", errors)

    item_roles: dict[str, str] = {}
    inventory = document.get("inventory")
    if not isinstance(inventory, list) or not inventory:
        errors.append("$.inventory: expected a non-empty array")
        inventory = []
    for index, item in enumerate(inventory):
        path = f"$.inventory[{index}]"
        if not _check_keys(
            item, {"id", "label", "role", "evidence"}, set(), path, errors
        ):
            continue
        item_id = _require_id(item.get("id"), "item:", f"{path}.id", errors)
        if item_id is not None:
            if item_id in item_roles:
                errors.append(f"{path}.id: duplicate inventory id {item_id!r}")
            item_roles[item_id] = item.get("role")
        if not _nonempty_string(item.get("label")):
            errors.append(f"{path}.label: expected a non-empty string")
        if item.get("role") not in ITEM_ROLES:
            errors.append(f"{path}.role: expected one of {sorted(ITEM_ROLES)}")
        _validate_evidence(item.get("evidence"), f"{path}.evidence", errors)

    seen_node_ids: set[str] = set()
    member_homes: dict[str, list[str]] = defaultdict(list)
    tree = document.get("tree")
    _validate_node(
        tree,
        "$.tree",
        mode,
        diagnosed_shape,
        item_roles,
        seen_node_ids,
        member_homes,
        errors,
    )

    relations = document.get("relations")
    seen_relation_ids: set[str] = set()
    if not isinstance(relations, list):
        errors.append("$.relations: expected an array")
        relations = []
    endpoints = set(item_roles) | seen_node_ids
    for index, relation in enumerate(relations):
        path = f"$.relations[{index}]"
        if not _check_keys(
            relation,
            {"id", "kind", "source_id", "target_id", "reason", "evidence"},
            set(),
            path,
            errors,
        ):
            continue
        relation_id = _require_id(
            relation.get("id"), "relation:", f"{path}.id", errors
        )
        if relation_id is not None:
            if relation_id in seen_relation_ids:
                errors.append(f"{path}.id: duplicate relation id {relation_id!r}")
            seen_relation_ids.add(relation_id)
        if relation.get("kind") not in RELATION_KINDS:
            errors.append(
                f"{path}.kind: expected one of {sorted(RELATION_KINDS)}"
            )
        for field in ("source_id", "target_id"):
            endpoint = relation.get(field)
            if endpoint not in endpoints:
                errors.append(f"{path}.{field}: unresolved endpoint {endpoint!r}")
        if relation.get("source_id") == relation.get("target_id"):
            errors.append(f"{path}: relation endpoints must differ")
        if not _nonempty_string(relation.get("reason")):
            errors.append(f"{path}.reason: expected a non-empty string")
        _validate_evidence(relation.get("evidence"), f"{path}.evidence", errors)

    residuals = document.get("residuals")
    excluded_counts: Counter[str] = Counter()
    unresolved_counts: Counter[str] = Counter()
    seam_records: list[tuple[str, str, list[str], str]] = []
    if not _check_keys(residuals, REQUIRED_RESIDUALS, set(), "$.residuals", errors):
        residuals = {}

    for name in REQUIRED_RESIDUALS:
        if not isinstance(residuals.get(name), list):
            errors.append(f"$.residuals.{name}: expected an array")

    for index, entry in enumerate(residuals.get("excluded_decorations", [])):
        path = f"$.residuals.excluded_decorations[{index}]"
        if not _check_keys(
            entry, {"item_id", "distributed_as", "evidence"}, set(), path, errors
        ):
            continue
        item_id = entry.get("item_id")
        if item_id not in item_roles:
            errors.append(f"{path}.item_id: unknown inventory item {item_id!r}")
        elif item_roles[item_id] != "decoration":
            errors.append(f"{path}.item_id: excluded item must be a decoration")
        else:
            excluded_counts[item_id] += 1
        if not _nonempty_string(entry.get("distributed_as")):
            errors.append(f"{path}.distributed_as: expected a non-empty string")
        _validate_string_list(entry.get("evidence"), f"{path}.evidence", errors, nonempty=True)

    for index, entry in enumerate(residuals.get("unresolved_items", [])):
        path = f"$.residuals.unresolved_items[{index}]"
        if not _check_keys(
            entry, {"item_id", "reason", "next_evidence"}, set(), path, errors
        ):
            continue
        item_id = entry.get("item_id")
        if item_id not in item_roles:
            errors.append(f"{path}.item_id: unknown inventory item {item_id!r}")
        elif item_roles[item_id] != "constituent":
            errors.append(f"{path}.item_id: unresolved item must be a constituent")
        else:
            unresolved_counts[item_id] += 1
        for field in ("reason", "next_evidence"):
            if not _nonempty_string(entry.get(field)):
                errors.append(f"{path}.{field}: expected a non-empty string")

    for index, entry in enumerate(residuals.get("seam_straddlers", [])):
        path = f"$.residuals.seam_straddlers[{index}]"
        if not _check_keys(
            entry,
            {"item_id", "home_node_id", "alternate_node_ids", "reason"},
            set(),
            path,
            errors,
        ):
            continue
        item_id = entry.get("item_id")
        home = entry.get("home_node_id")
        alternates = entry.get("alternate_node_ids")
        if item_roles.get(item_id) != "constituent":
            errors.append(f"{path}.item_id: expected a constituent inventory id")
        if home not in seen_node_ids:
            errors.append(f"{path}.home_node_id: unknown node {home!r}")
        if not isinstance(alternates, list) or not alternates:
            errors.append(f"{path}.alternate_node_ids: expected a non-empty array")
            alternates = []
        elif len(alternates) != len(set(alternates)):
            errors.append(f"{path}.alternate_node_ids: duplicate node id")
        for alternate in alternates:
            if alternate not in seen_node_ids:
                errors.append(f"{path}.alternate_node_ids: unknown node {alternate!r}")
            if alternate == home:
                errors.append(f"{path}.alternate_node_ids: home cannot be an alternate")
        if not _nonempty_string(entry.get("reason")):
            errors.append(f"{path}.reason: expected a non-empty string")
        if isinstance(item_id, str) and isinstance(home, str):
            seam_records.append((item_id, home, alternates, path))

    for index, entry in enumerate(residuals.get("judgment_calls", [])):
        path = f"$.residuals.judgment_calls[{index}]"
        if not _check_keys(
            entry,
            {"decision", "alternative", "reason", "node_ids"},
            set(),
            path,
            errors,
        ):
            continue
        for field in ("decision", "alternative", "reason"):
            if not _nonempty_string(entry.get(field)):
                errors.append(f"{path}.{field}: expected a non-empty string")
        node_ids = entry.get("node_ids")
        if not isinstance(node_ids, list) or not node_ids:
            errors.append(f"{path}.node_ids: expected a non-empty array")
        else:
            for node_id in node_ids:
                if node_id not in seen_node_ids:
                    errors.append(f"{path}.node_ids: unknown node {node_id!r}")

    for index, entry in enumerate(residuals.get("low_confidence", [])):
        path = f"$.residuals.low_confidence[{index}]"
        if not _check_keys(entry, {"node_id", "reason"}, set(), path, errors):
            continue
        if entry.get("node_id") not in seen_node_ids:
            errors.append(f"{path}.node_id: unknown node {entry.get('node_id')!r}")
        if not _nonempty_string(entry.get("reason")):
            errors.append(f"{path}.reason: expected a non-empty string")

    for index, entry in enumerate(residuals.get("semi_lattice_signals", [])):
        path = f"$.residuals.semi_lattice_signals[{index}]"
        if not _check_keys(
            entry, {"item_ids", "node_ids", "reason"}, set(), path, errors
        ):
            continue
        item_ids = entry.get("item_ids")
        node_ids = entry.get("node_ids")
        if not isinstance(item_ids, list) or not item_ids:
            errors.append(f"{path}.item_ids: expected a non-empty array")
        else:
            for item_id in item_ids:
                if item_id not in item_roles:
                    errors.append(f"{path}.item_ids: unknown item {item_id!r}")
        if not isinstance(node_ids, list) or len(node_ids) < 2:
            errors.append(f"{path}.node_ids: expected at least two nodes")
        else:
            for node_id in node_ids:
                if node_id not in seen_node_ids:
                    errors.append(f"{path}.node_ids: unknown node {node_id!r}")
        if not _nonempty_string(entry.get("reason")):
            errors.append(f"{path}.reason: expected a non-empty string")

    for index, entry in enumerate(residuals.get("population_warnings", [])):
        path = f"$.residuals.population_warnings[{index}]"
        if not _check_keys(entry, {"item_id", "reason"}, set(), path, errors):
            continue
        item_id = entry.get("item_id")
        if item_id is not None and item_id not in item_roles:
            errors.append(f"{path}.item_id: unknown inventory item {item_id!r}")
        if not _nonempty_string(entry.get("reason")):
            errors.append(f"{path}.reason: expected a non-empty string")

    constituent_ids = {
        item_id for item_id, role in item_roles.items() if role == "constituent"
    }
    decoration_ids = {
        item_id for item_id, role in item_roles.items() if role == "decoration"
    }
    for item_id in sorted(constituent_ids):
        homes = len(member_homes.get(item_id, []))
        unresolved = unresolved_counts[item_id]
        if homes + unresolved != 1:
            errors.append(
                f"$.inventory: constituent {item_id!r} must have exactly one primary "
                f"leaf home or unresolved record; found {homes} homes and {unresolved} unresolved records"
            )
    for item_id in sorted(decoration_ids):
        if excluded_counts[item_id] != 1:
            errors.append(
                f"$.inventory: decoration {item_id!r} must appear exactly once in "
                f"excluded_decorations; found {excluded_counts[item_id]}"
            )
    for item_id, home, _alternates, path in seam_records:
        if member_homes.get(item_id) != [home]:
            errors.append(
                f"{path}.home_node_id: must equal the item's unique primary leaf home"
            )

    review = document.get("semantic_review")
    review_checks: dict[str, Any] = {}
    if _check_keys(review, {"status", "checks"}, set(), "$.semantic_review", errors):
        semantic_status = review.get("status")
        if semantic_status not in {"provisional", "reviewed"}:
            errors.append("$.semantic_review.status: expected 'provisional' or 'reviewed'")
        if mode == "light" and semantic_status != "provisional":
            errors.append("$.semantic_review.status: light mode must remain provisional")
        if mode in {"medium", "heavy"} and semantic_status != "reviewed":
            errors.append(f"$.semantic_review.status: {mode} mode must be reviewed")
        checks = review.get("checks")
        if _check_keys(
            checks, REQUIRED_CHECKS, set(), "$.semantic_review.checks", errors
        ):
            review_checks = checks
            for name in REQUIRED_CHECKS:
                _validate_review_check(
                    checks.get(name), f"$.semantic_review.checks.{name}", errors
                )

    required_by_mode = {
        "medium": {"population_sanity", "one_ply_lookahead", "kind_homogeneity"},
        "heavy": {
            "population_sanity",
            "paradigm_sweep",
            "native_n_array",
            "one_ply_lookahead",
            "kind_homogeneity",
        },
    }
    for name in required_by_mode.get(mode, {"population_sanity"}):
        check = review_checks.get(name)
        if isinstance(check, dict) and check.get("status") == "not_run":
            errors.append(
                f"$.semantic_review.checks.{name}: {mode} mode requires this check"
            )
    if operation == "reconcile" and mode in {"medium", "heavy"}:
        check = review_checks.get("incumbent_challenge")
        if isinstance(check, dict) and check.get("status") == "not_run":
            errors.append(
                "$.semantic_review.checks.incumbent_challenge: reconciliation requires this check"
            )

    flagged_checks = [
        name
        for name, check in review_checks.items()
        if isinstance(check, dict) and check.get("status") == "flagged"
    ]
    substantive_residuals = (
        "unresolved_items",
        "seam_straddlers",
        "judgment_calls",
        "low_confidence",
        "semi_lattice_signals",
        "population_warnings",
    )
    if flagged_checks and not any(residuals.get(name) for name in substantive_residuals):
        errors.append(
            "$.residuals: flagged semantic checks require at least one substantive residual"
        )

    population_check = review_checks.get("population_sanity")
    if (
        requested_shape in SHAPES
        and diagnosed_shape in SHAPES
        and requested_shape != diagnosed_shape
    ):
        if not (
            isinstance(population_check, dict)
            and population_check.get("status") == "flagged"
        ):
            errors.append(
                "$.semantic_review.checks.population_sanity: shape mismatch must be flagged"
            )
        if not residuals.get("population_warnings"):
            errors.append(
                "$.residuals.population_warnings: shape mismatch requires a warning"
            )

    if diagnosed_shape == "population" and isinstance(tree, dict):
        if tree.get("children"):
            errors.append("$.tree.children: a population must remain flat")
        facets = tree.get("facets")
        if not isinstance(facets, list) or not facets:
            errors.append("$.tree.facets: a population requires at least one facet")
        if document.get("organizing_principle") is not None:
            errors.append("$.organizing_principle: a population requires null")
    elif diagnosed_shape == "decomposition":
        if not _nonempty_string(document.get("organizing_principle")):
            errors.append(
                "$.organizing_principle: a decomposition requires a non-empty string"
            )

    _validate_lineage(
        document,
        parent_document,
        operation,
        seen_node_ids,
        errors,
    )

    return errors


def _validate_node(
    node: Any,
    path: str,
    mode: Any,
    diagnosed_shape: Any,
    item_roles: dict[str, str],
    seen_node_ids: set[str],
    member_homes: dict[str, list[str]],
    errors: list[str],
) -> None:
    required = {
        "id",
        "label",
        "kind",
        "gloss",
        "cohesion_basis",
        "member_ids",
        "children",
        "facets",
    }
    optional = {"dichotomy_reason", "fanout_exception"}
    if not _check_keys(node, required, optional, path, errors):
        return

    node_id = _require_id(node.get("id"), "node:", f"{path}.id", errors)
    if node_id is not None:
        if node_id in seen_node_ids:
            errors.append(f"{path}.id: duplicate node id {node_id!r}")
        seen_node_ids.add(node_id)

    for field in ("label", "kind", "gloss", "cohesion_basis"):
        if not _nonempty_string(node.get(field)):
            errors.append(f"{path}.{field}: expected a non-empty string")

    member_ids = node.get("member_ids")
    if not isinstance(member_ids, list):
        errors.append(f"{path}.member_ids: expected an array")
        member_ids = []
    if len(member_ids) != len(set(member_ids)):
        errors.append(f"{path}.member_ids: duplicate item id")
    for item_id in member_ids:
        if item_id not in item_roles:
            errors.append(f"{path}.member_ids: unknown inventory item {item_id!r}")
        elif item_roles[item_id] != "constituent":
            errors.append(f"{path}.member_ids: decorations cannot be node members")
        elif node_id is not None:
            member_homes[item_id].append(node_id)

    children = node.get("children")
    if not isinstance(children, list):
        errors.append(f"{path}.children: expected an array")
        children = []
    facets = node.get("facets")
    if not isinstance(facets, list):
        errors.append(f"{path}.facets: expected an array")
        facets = []
    else:
        _validate_string_list(facets, f"{path}.facets", errors)

    if children and member_ids:
        errors.append(f"{path}.member_ids: internal nodes cannot directly home items")
    if diagnosed_shape == "decomposition" and facets:
        errors.append(f"{path}.facets: decomposition nodes must not carry population facets")

    child_count = len(children)
    if child_count == 1:
        errors.append(f"{path}.children: one-child layers must collapse")
    if child_count == 2 and not _nonempty_string(node.get("dichotomy_reason")):
        errors.append(
            f"{path}.dichotomy_reason: two-child layers require a genuine fork reason"
        )
    if child_count != 2 and "dichotomy_reason" in node:
        errors.append(f"{path}.dichotomy_reason: allowed only on a two-child node")
    if child_count > 7:
        fanout = node.get("fanout_exception")
        fanout_path = f"{path}.fanout_exception"
        if _check_keys(
            fanout, {"reason", "rejected_grouping"}, set(), fanout_path, errors
        ):
            for field in ("reason", "rejected_grouping"):
                if not _nonempty_string(fanout.get(field)):
                    errors.append(f"{fanout_path}.{field}: expected a non-empty string")
    elif "fanout_exception" in node:
        errors.append(f"{path}.fanout_exception: allowed only when child count exceeds seven")

    if mode in {"medium", "heavy"} and children:
        child_kinds = {
            child.get("kind")
            for child in children
            if isinstance(child, dict) and _nonempty_string(child.get("kind"))
        }
        if len(child_kinds) > 1:
            errors.append(
                f"{path}.children: reviewed sibling set declares heterogeneous kinds "
                f"{sorted(child_kinds)}"
            )

    for index, child in enumerate(children):
        _validate_node(
            child,
            f"{path}.children[{index}]",
            mode,
            diagnosed_shape,
            item_roles,
            seen_node_ids,
            member_homes,
            errors,
        )


def _validate_review_check(value: Any, path: str, errors: list[str]) -> None:
    if not _check_keys(value, {"status", "claim", "evidence"}, set(), path, errors):
        return
    status = value.get("status")
    if status not in CHECK_STATUSES:
        errors.append(f"{path}.status: expected one of {sorted(CHECK_STATUSES)}")
    if not _nonempty_string(value.get("claim")):
        errors.append(f"{path}.claim: expected a non-empty string")
    evidence = value.get("evidence")
    strings = _validate_string_list(evidence, f"{path}.evidence", errors)
    if status in {"passed", "flagged"} and not strings:
        errors.append(f"{path}.evidence: passed or flagged checks require evidence")


def _validate_lineage(
    document: dict[str, Any],
    parent_document: Any | None,
    operation: Any,
    current_node_ids: set[str],
    errors: list[str],
) -> None:
    lineage = document.get("lineage")
    path = "$.lineage"
    required = {
        "parent_artifact_id",
        "reconciliation_scope",
        "decision",
        "preserved_node_ids",
        "added_node_ids",
        "retired_node_ids",
    }
    if not _check_keys(lineage, required, set(), path, errors):
        return
    if not _nonempty_string(lineage.get("decision")):
        errors.append(f"{path}.decision: expected a non-empty string")

    sets: dict[str, set[str]] = {}
    for field in ("preserved_node_ids", "added_node_ids", "retired_node_ids"):
        value = lineage.get(field)
        if not isinstance(value, list):
            errors.append(f"{path}.{field}: expected an array")
            value = []
        if len(value) != len(set(value)):
            errors.append(f"{path}.{field}: duplicate node id")
        for index, node_id in enumerate(value):
            _require_id(node_id, "node:", f"{path}.{field}[{index}]", errors)
        sets[field] = set(value)

    preserved = sets["preserved_node_ids"]
    added = sets["added_node_ids"]
    retired = sets["retired_node_ids"]
    if preserved & added or preserved & retired or added & retired:
        errors.append(f"{path}: preserved, added, and retired node sets must be disjoint")

    if operation == "initial":
        if lineage.get("parent_artifact_id") is not None:
            errors.append(f"{path}.parent_artifact_id: initial carve requires null")
        if lineage.get("reconciliation_scope") != "initial":
            errors.append(f"{path}.reconciliation_scope: initial carve requires 'initial'")
        if preserved or retired:
            errors.append(f"{path}: initial carve cannot preserve or retire node ids")
        if added != current_node_ids:
            errors.append(f"{path}.added_node_ids: initial carve must list every current node")
        return

    if operation != "reconcile":
        return

    parent_artifact_id = lineage.get("parent_artifact_id")
    _require_id(parent_artifact_id, "carve:", f"{path}.parent_artifact_id", errors)
    if lineage.get("reconciliation_scope") not in {"local", "global"}:
        errors.append(
            f"{path}.reconciliation_scope: reconciliation requires 'local' or 'global'"
        )
    if preserved | added != current_node_ids:
        errors.append(
            f"{path}: preserved plus added node ids must equal the current tree ids"
        )
    if retired & current_node_ids:
        errors.append(f"{path}.retired_node_ids: retired ids cannot remain in the tree")
    if not isinstance(parent_document, dict):
        errors.append(f"{path}: reconciliation validation requires --parent")
        return
    if parent_document.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"{path}: parent must use schema version {SCHEMA_VERSION}")
    if parent_document.get("artifact_id") != parent_artifact_id:
        errors.append(f"{path}.parent_artifact_id: does not match supplied parent")
    parent_node_ids = _collect_tree_ids(parent_document.get("tree"))
    expected_preserved = parent_node_ids & current_node_ids
    expected_added = current_node_ids - parent_node_ids
    expected_retired = parent_node_ids - current_node_ids
    if preserved != expected_preserved:
        errors.append(f"{path}.preserved_node_ids: does not match parent/current identity")
    if added != expected_added:
        errors.append(f"{path}.added_node_ids: does not match parent/current identity")
    if retired != expected_retired:
        errors.append(f"{path}.retired_node_ids: does not match parent/current identity")


def _receipt(
    path: Path,
    raw: bytes,
    document: dict[str, Any],
    parent_path: Path | None = None,
    parent_raw: bytes | None = None,
    parent_document: dict[str, Any] | None = None,
) -> dict[str, Any]:
    receipt = {
        "receipt_schema_version": 1,
        "validator_version": VALIDATOR_VERSION,
        "contract_schema_version": SCHEMA_VERSION,
        "artifact_id": document["artifact_id"],
        "artifact_path": str(path.resolve()),
        "artifact_sha256": hashlib.sha256(raw).hexdigest(),
        "valid": True,
    }
    if (
        parent_path is not None
        and parent_raw is not None
        and parent_document is not None
    ):
        receipt.update(
            {
                "parent_artifact_id": parent_document["artifact_id"],
                "parent_artifact_path": str(parent_path.resolve()),
                "parent_artifact_sha256": hashlib.sha256(parent_raw).hexdigest(),
            }
        )
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate canonical output from the modularize skill."
    )
    parser.add_argument("artifact", type=Path, help="Path to a modularize JSON file")
    parser.add_argument(
        "--parent",
        type=Path,
        help="Prior schema-version-2 artifact required for reconciliation",
    )
    parser.add_argument(
        "--receipt",
        type=Path,
        help="Write a hash-bound validation receipt after a successful pass",
    )
    args = parser.parse_args(argv)

    try:
        raw = args.artifact.read_bytes()
        document = json.loads(raw.decode("utf-8"))
    except FileNotFoundError:
        print(f"error: artifact not found: {args.artifact}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"error: cannot read artifact {args.artifact}: {error}", file=sys.stderr)
        return 2
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"error: invalid UTF-8 JSON in {args.artifact}: {error}", file=sys.stderr)
        return 2

    parent_raw: bytes | None = None
    parent_document: Any | None = None
    if args.parent is not None:
        try:
            parent_raw = args.parent.read_bytes()
            parent_document = json.loads(parent_raw.decode("utf-8"))
        except FileNotFoundError:
            print(f"error: parent artifact not found: {args.parent}", file=sys.stderr)
            return 2
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            print(f"error: cannot read parent artifact {args.parent}: {error}", file=sys.stderr)
            return 2

    errors = validate_document(document, parent_document)
    if errors:
        print(f"{args.artifact}: invalid modularize artifact", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if args.receipt is not None:
        try:
            args.receipt.write_text(
                json.dumps(
                    _receipt(
                        args.artifact,
                        raw,
                        document,
                        args.parent,
                        parent_raw,
                        parent_document,
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        except OSError as error:
            print(f"error: cannot write receipt {args.receipt}: {error}", file=sys.stderr)
            return 2

    print(
        f"{args.artifact}: contract-valid modularize artifact "
        f"(schema {SCHEMA_VERSION}, validator {VALIDATOR_VERSION})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
