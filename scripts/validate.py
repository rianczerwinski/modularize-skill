#!/usr/bin/env python3
"""Validate a modularize JSON artifact against the portable output contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MODES = {"light", "medium", "heavy"}
SHAPES = {"decomposition", "population"}
CHECK_STATUSES = {"not_run", "passed", "flagged"}
REQUIRED_CHECKS = {
    "population_sanity",
    "paradigm_sweep",
    "native_n_array",
    "one_ply_lookahead",
    "kind_homogeneity",
}
REQUIRED_RESIDUALS = {
    "excluded_decorations",
    "seam_straddlers",
    "judgment_calls",
    "low_confidence",
    "semi_lattice_signals",
    "population_warnings",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_document(document: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(document, dict):
        return ["$: expected a JSON object"]

    if document.get("schema_version") != 1:
        errors.append("$.schema_version: expected 1")

    for field in ("subject",):
        if not _nonempty_string(document.get(field)):
            errors.append(f"$.{field}: expected a non-empty string")

    mode = document.get("mode")
    if mode not in MODES:
        errors.append(f"$.mode: expected one of {sorted(MODES)}")

    requested_shape = document.get("requested_shape")
    diagnosed_shape = document.get("diagnosed_shape")
    if requested_shape not in SHAPES:
        errors.append(f"$.requested_shape: expected one of {sorted(SHAPES)}")
    if diagnosed_shape not in SHAPES:
        errors.append(f"$.diagnosed_shape: expected one of {sorted(SHAPES)}")

    status = document.get("status")
    if status not in {"unverified", "verified"}:
        errors.append("$.status: expected 'unverified' or 'verified'")
    if mode == "light" and status != "unverified":
        errors.append("$.status: light mode must remain unverified")
    if mode in {"medium", "heavy"} and status != "verified":
        errors.append(f"$.status: {mode} mode must be verified after required checks")

    verification = document.get("verification")
    if not isinstance(verification, dict):
        errors.append("$.verification: expected an object")
        verification = {}
    else:
        missing = REQUIRED_CHECKS - verification.keys()
        for name in sorted(missing):
            errors.append(f"$.verification.{name}: missing required check")
        for name in REQUIRED_CHECKS & verification.keys():
            check = verification[name]
            if not isinstance(check, dict):
                errors.append(f"$.verification.{name}: expected an object")
                continue
            if check.get("status") not in CHECK_STATUSES:
                errors.append(
                    f"$.verification.{name}.status: expected one of {sorted(CHECK_STATUSES)}"
                )
            if not isinstance(check.get("note"), str):
                errors.append(f"$.verification.{name}.note: expected a string")

    required_by_mode = {
        "medium": {"one_ply_lookahead", "kind_homogeneity"},
        "heavy": {
            "paradigm_sweep",
            "native_n_array",
            "one_ply_lookahead",
            "kind_homogeneity",
        },
    }
    for name in required_by_mode.get(mode, set()):
        check = verification.get(name)
        if isinstance(check, dict) and check.get("status") == "not_run":
            errors.append(f"$.verification.{name}: {mode} mode requires this check")

    population_check = verification.get("population_sanity")
    if isinstance(population_check, dict) and population_check.get("status") == "not_run":
        errors.append("$.verification.population_sanity: this check is always required")

    residuals = document.get("residuals")
    if not isinstance(residuals, dict):
        errors.append("$.residuals: expected an object")
        residuals = {}
    else:
        missing = REQUIRED_RESIDUALS - residuals.keys()
        for name in sorted(missing):
            errors.append(f"$.residuals.{name}: missing required residual array")
        for name in REQUIRED_RESIDUALS & residuals.keys():
            if not isinstance(residuals[name], list):
                errors.append(f"$.residuals.{name}: expected an array")

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
                "$.verification.population_sanity: shape mismatch must be flagged"
            )
        warnings = residuals.get("population_warnings")
        if not isinstance(warnings, list) or not warnings:
            errors.append(
                "$.residuals.population_warnings: shape mismatch requires a warning"
            )

    tree = document.get("tree")
    seen_ids: set[str] = set()
    _validate_node(tree, "$.tree", mode, seen_ids, errors)

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

    return errors


def _validate_node(
    node: Any,
    path: str,
    mode: Any,
    seen_ids: set[str],
    errors: list[str],
) -> None:
    if not isinstance(node, dict):
        errors.append(f"{path}: expected an object")
        return

    for field in ("id", "label", "kind", "gloss", "cohesion_basis"):
        if not _nonempty_string(node.get(field)):
            errors.append(f"{path}.{field}: expected a non-empty string")

    node_id = node.get("id")
    if isinstance(node_id, str):
        if node_id in seen_ids:
            errors.append(f"{path}.id: duplicate id {node_id!r}")
        seen_ids.add(node_id)

    children = node.get("children")
    if not isinstance(children, list):
        errors.append(f"{path}.children: expected an array")
        children = []

    facets = node.get("facets")
    if not isinstance(facets, list):
        errors.append(f"{path}.facets: expected an array")

    child_count = len(children)
    if child_count == 1:
        errors.append(f"{path}.children: one-child layers must collapse")
    if child_count == 2 and not _nonempty_string(node.get("dichotomy_reason")):
        errors.append(
            f"{path}.dichotomy_reason: two-child layers require a genuine fork reason"
        )
    if child_count > 7:
        errors.append(f"{path}.children: {child_count} exceeds the diagnostic maximum of 7")

    if mode in {"medium", "heavy"} and children:
        child_kinds = {
            child.get("kind")
            for child in children
            if isinstance(child, dict) and _nonempty_string(child.get("kind"))
        }
        if len(child_kinds) > 1:
            errors.append(
                f"{path}.children: verified sibling set declares heterogeneous kinds "
                f"{sorted(child_kinds)}"
            )

    for index, child in enumerate(children):
        _validate_node(child, f"{path}.children[{index}]", mode, seen_ids, errors)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate canonical output from the modularize skill."
    )
    parser.add_argument("artifact", type=Path, help="Path to a modularize JSON file")
    args = parser.parse_args(argv)

    try:
        document = json.loads(args.artifact.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"error: artifact not found: {args.artifact}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"error: cannot read {args.artifact}: {error}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as error:
        print(
            f"error: invalid JSON in {args.artifact}:{error.lineno}:{error.colno}: "
            f"{error.msg}",
            file=sys.stderr,
        )
        return 2

    errors = validate_document(document)
    if errors:
        print(f"{args.artifact}: invalid modularize artifact", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"{args.artifact}: valid modularize artifact")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
