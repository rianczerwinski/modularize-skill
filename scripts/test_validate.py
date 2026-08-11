#!/usr/bin/env python3
"""Contract tests and mutation-checked negative controls for modularize v2."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from types import ModuleType


SKILL_ROOT = Path(__file__).resolve().parents[1]


def _load_validator() -> ModuleType:
    path = SKILL_ROOT / "scripts" / "validate.py"
    spec = importlib.util.spec_from_file_location("modularize_validate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_validator()


def _valid_document() -> dict:
    return json.loads(
        (SKILL_ROOT / "examples" / "feedback-loop.json").read_text(encoding="utf-8")
    )


def _errors(document: dict, parent: dict | None = None) -> list[str]:
    return VALIDATOR.validate_document(document, parent)


def _document_with_fanout(count: int, *, exception: bool) -> dict:
    document = _valid_document()
    root = document["tree"]
    template_node = root["children"][0]
    decoration = next(
        item for item in document["inventory"] if item["role"] == "decoration"
    )
    document["inventory"] = [decoration]
    document["relations"] = []
    document["residuals"]["seam_straddlers"] = []
    root["children"] = []
    added_ids = [root["id"]]
    for index in range(1, count + 1):
        item_id = f"item:{uuid.UUID(int=index)}"
        node_id = f"node:{uuid.UUID(int=100 + index)}"
        document["inventory"].append(
            {
                "id": item_id,
                "label": f"Stage evidence {index}",
                "role": "constituent",
                "evidence": [
                    {"ref": "test:fanout", "note": "Fixture constituent."}
                ],
            }
        )
        node = copy.deepcopy(template_node)
        node["id"] = node_id
        node["label"] = f"Stage {index}"
        node["member_ids"] = [item_id]
        root["children"].append(node)
        added_ids.append(node_id)
    document["lineage"]["added_node_ids"] = added_ids
    if exception:
        root["fanout_exception"] = {
            "reason": "The eight stages are one irreducible protocol alphabet.",
            "rejected_grouping": "Pairing stages would mix distinct protocol meanings and add a false tier.",
        }
    return document


class ValidatorContractTests(unittest.TestCase):
    def test_contract_accepts_positive_v2_example(self) -> None:
        self.assertEqual(_errors(_valid_document()), [])

    def test_contract_receipt_binds_artifact_hash(self) -> None:
        document = _valid_document()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "artifact.json"
            receipt = root / "receipt.json"
            artifact.write_text(json.dumps(document), encoding="utf-8")
            self.assertEqual(
                VALIDATOR.main([str(artifact), "--receipt", str(receipt)]), 0
            )
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertTrue(data["valid"])
            self.assertEqual(data["contract_schema_version"], 2)
            self.assertEqual(data["artifact_id"], document["artifact_id"])
            self.assertEqual(len(data["artifact_sha256"]), 64)

    def test_contract_accepts_eight_children_with_real_exception(self) -> None:
        document = _document_with_fanout(8, exception=True)
        self.assertEqual(_errors(document), [])

    def test_contract_accepts_reconciliation_against_parent(self) -> None:
        parent = _valid_document()
        document = copy.deepcopy(parent)
        document["artifact_id"] = "carve:22222222-2222-4222-8222-222222222222"
        document["operation"] = "reconcile"
        document["lineage"] = {
            "parent_artifact_id": parent["artifact_id"],
            "reconciliation_scope": "local",
            "decision": "A fresh challenger confirmed the root and changed no referents.",
            "preserved_node_ids": parent["lineage"]["added_node_ids"],
            "added_node_ids": [],
            "retired_node_ids": [],
        }
        document["semantic_review"]["checks"]["incumbent_challenge"] = {
            "status": "passed",
            "claim": "The incumbent root outperformed the fresh ownership-based challenger.",
            "evidence": ["candidate comparison: transformation versus ownership"],
        }
        self.assertEqual(_errors(document, parent), [])

    def test_reconciliation_receipt_binds_parent_artifact_hash(self) -> None:
        parent = _valid_document()
        document = copy.deepcopy(parent)
        document["artifact_id"] = "carve:22222222-2222-4222-8222-222222222222"
        document["operation"] = "reconcile"
        document["lineage"] = {
            "parent_artifact_id": parent["artifact_id"],
            "reconciliation_scope": "global",
            "decision": "A fresh challenger confirmed the complete incumbent tree.",
            "preserved_node_ids": parent["lineage"]["added_node_ids"],
            "added_node_ids": [],
            "retired_node_ids": [],
        }
        document["semantic_review"]["checks"]["incumbent_challenge"] = {
            "status": "passed",
            "claim": "A fresh challenger converged on the incumbent tree.",
            "evidence": ["candidate comparison: incumbent versus fresh carve"],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "artifact.json"
            parent_artifact = root / "parent.json"
            receipt = root / "receipt.json"
            artifact.write_text(json.dumps(document), encoding="utf-8")
            parent_artifact.write_text(json.dumps(parent), encoding="utf-8")
            self.assertEqual(
                VALIDATOR.main(
                    [
                        str(artifact),
                        "--parent",
                        str(parent_artifact),
                        "--receipt",
                        str(receipt),
                    ]
                ),
                0,
            )
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(data["parent_artifact_id"], parent["artifact_id"])
            self.assertEqual(len(data["parent_artifact_sha256"]), 64)

    def test_negative_control_rejects_schema_v1(self) -> None:
        document = _valid_document()
        document["schema_version"] = 1
        errors = _errors(document)
        self.assertTrue(any("schema_version: expected 2" in error for error in errors))

    def test_negative_control_rejects_legacy_verified_status(self) -> None:
        document = _valid_document()
        document["status"] = "verified"
        errors = _errors(document)
        self.assertTrue(any("$.status: unknown field" in error for error in errors))

    def test_negative_control_rejects_unaccounted_constituent(self) -> None:
        document = _valid_document()
        item_id = document["tree"]["children"][0]["member_ids"].pop()
        errors = _errors(document)
        self.assertTrue(
            any(item_id in error and "exactly one primary leaf home" in error for error in errors)
        )

    def test_negative_control_rejects_duplicate_primary_home(self) -> None:
        document = _valid_document()
        item_id = document["tree"]["children"][0]["member_ids"][0]
        document["tree"]["children"][1]["member_ids"].append(item_id)
        errors = _errors(document)
        self.assertTrue(
            any(item_id in error and "found 2 homes" in error for error in errors)
        )

    def test_negative_control_rejects_empty_leaf(self) -> None:
        document = _valid_document()
        leaf = document["tree"]["children"][0]
        for item_id in leaf["member_ids"]:
            document["residuals"]["unresolved_items"].append(
                {
                    "item_id": item_id,
                    "reason": "Keep inventory accounting valid while testing the empty leaf.",
                    "next_evidence": "The leaf itself must still be rejected.",
                }
            )
        leaf["member_ids"] = []
        errors = _errors(document)
        self.assertTrue(any("leaf nodes must home at least one constituent" in error for error in errors))

    def test_negative_control_rejects_decoration_as_node_member(self) -> None:
        document = _valid_document()
        decoration_id = document["residuals"]["excluded_decorations"][0]["item_id"]
        document["tree"]["children"][0]["member_ids"].append(decoration_id)
        errors = _errors(document)
        self.assertTrue(any("decorations cannot be node members" in error for error in errors))

    def test_negative_control_rejects_positional_node_identity(self) -> None:
        document = _valid_document()
        document["tree"]["children"][0]["id"] = "1.1"
        errors = _errors(document)
        self.assertTrue(any("expected node:<canonical-uuid>" in error for error in errors))

    def test_negative_control_rejects_eight_children_without_exception(self) -> None:
        document = _document_with_fanout(8, exception=False)
        errors = _errors(document)
        self.assertTrue(any("fanout_exception" in error for error in errors))

    def test_negative_control_rejects_unrun_medium_probe(self) -> None:
        document = _valid_document()
        document["semantic_review"]["checks"]["kind_homogeneity"]["status"] = "not_run"
        document["semantic_review"]["checks"]["kind_homogeneity"]["evidence"] = []
        errors = _errors(document)
        self.assertTrue(any("medium mode requires this check" in error for error in errors))

    def test_negative_control_rejects_evidence_free_pass(self) -> None:
        document = _valid_document()
        document["semantic_review"]["checks"]["kind_homogeneity"]["evidence"] = []
        errors = _errors(document)
        self.assertTrue(any("checks require evidence" in error for error in errors))

    def test_negative_control_rejects_flag_without_residual(self) -> None:
        document = _valid_document()
        document["semantic_review"]["checks"]["kind_homogeneity"]["status"] = "flagged"
        for name in (
            "unresolved_items",
            "seam_straddlers",
            "judgment_calls",
            "low_confidence",
            "semi_lattice_signals",
            "population_warnings",
        ):
            document["residuals"][name] = []
        errors = _errors(document)
        self.assertTrue(any("substantive residual" in error for error in errors))

    def test_negative_control_rejects_heterogeneous_sibling_kinds(self) -> None:
        document = _valid_document()
        document["tree"]["children"][1]["kind"] = "organizational owner"
        errors = _errors(document)
        self.assertTrue(any("heterogeneous kinds" in error for error in errors))

    def test_negative_control_rejects_unknown_relation_endpoint(self) -> None:
        document = _valid_document()
        document["relations"][0]["target_id"] = "node:99999999-9999-4999-8999-999999999999"
        errors = _errors(document)
        self.assertTrue(any("unresolved endpoint" in error for error in errors))

    def test_negative_control_reconciliation_requires_parent(self) -> None:
        parent = _valid_document()
        document = copy.deepcopy(parent)
        document["artifact_id"] = "carve:22222222-2222-4222-8222-222222222222"
        document["operation"] = "reconcile"
        document["lineage"] = {
            "parent_artifact_id": parent["artifact_id"],
            "reconciliation_scope": "local",
            "decision": "The root survived its challenger.",
            "preserved_node_ids": parent["lineage"]["added_node_ids"],
            "added_node_ids": [],
            "retired_node_ids": [],
        }
        document["semantic_review"]["checks"]["incumbent_challenge"] = {
            "status": "passed",
            "claim": "The incumbent root outperformed a fresh challenger.",
            "evidence": ["candidate comparison"],
        }
        errors = _errors(document)
        self.assertTrue(any("requires --parent" in error for error in errors))

    def test_negative_control_rejects_false_reconciliation_identity(self) -> None:
        parent = _valid_document()
        document = copy.deepcopy(parent)
        document["artifact_id"] = "carve:22222222-2222-4222-8222-222222222222"
        document["operation"] = "reconcile"
        preserved = parent["lineage"]["added_node_ids"][:-1]
        document["lineage"] = {
            "parent_artifact_id": parent["artifact_id"],
            "reconciliation_scope": "global",
            "decision": "Claim one continuing node was retired despite remaining present.",
            "preserved_node_ids": preserved,
            "added_node_ids": [],
            "retired_node_ids": [parent["lineage"]["added_node_ids"][-1]],
        }
        document["semantic_review"]["checks"]["incumbent_challenge"] = {
            "status": "passed",
            "claim": "A challenger was compared.",
            "evidence": ["candidate comparison"],
        }
        errors = _errors(document, parent)
        self.assertTrue(
            any("preserved plus added node ids" in error for error in errors)
        )


if __name__ == "__main__":
    unittest.main()
