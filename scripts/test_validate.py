#!/usr/bin/env python3
"""Contract tests and negative controls for the modularize artifact validator."""

from __future__ import annotations

import copy
import importlib.util
import json
import unittest
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


class ValidatorContractTests(unittest.TestCase):
    def test_contract_accepts_positive_example(self) -> None:
        self.assertEqual(VALIDATOR.validate_document(_valid_document()), [])

    def test_negative_control_rejects_light_result_marked_verified(self) -> None:
        document = _valid_document()
        document["mode"] = "light"
        errors = VALIDATOR.validate_document(document)
        self.assertTrue(any("light mode must remain unverified" in error for error in errors))

    def test_negative_control_rejects_unrun_medium_probe(self) -> None:
        document = _valid_document()
        document["verification"]["kind_homogeneity"]["status"] = "not_run"
        errors = VALIDATOR.validate_document(document)
        self.assertTrue(any("medium mode requires this check" in error for error in errors))

    def test_negative_control_rejects_heterogeneous_sibling_kinds(self) -> None:
        document = _valid_document()
        document["tree"]["children"][1]["kind"] = "organizational owner"
        errors = VALIDATOR.validate_document(document)
        self.assertTrue(any("heterogeneous kinds" in error for error in errors))

    def test_negative_control_rejects_duplicate_ids(self) -> None:
        document = _valid_document()
        document["tree"]["children"][1]["id"] = document["tree"]["children"][0]["id"]
        errors = VALIDATOR.validate_document(document)
        self.assertTrue(any("duplicate id" in error for error in errors))

    def test_negative_control_rejects_flat_population_with_children(self) -> None:
        document = _valid_document()
        document["diagnosed_shape"] = "population"
        document["requested_shape"] = "population"
        document["organizing_principle"] = None
        document["tree"]["facets"] = ["owner"]
        errors = VALIDATOR.validate_document(document)
        self.assertTrue(any("population must remain flat" in error for error in errors))

    def test_negative_control_rejects_more_than_seven_children(self) -> None:
        document = _valid_document()
        template = document["tree"]["children"][0]
        document["tree"]["children"] = []
        for index in range(8):
            child = copy.deepcopy(template)
            child["id"] = f"1.{index + 1}"
            child["label"] = f"Stage {index + 1}"
            document["tree"]["children"].append(child)
        errors = VALIDATOR.validate_document(document)
        self.assertTrue(any("exceeds the diagnostic maximum" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
