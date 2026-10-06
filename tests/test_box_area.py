from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from labeling_service import (
    AnnotationValidationError,
    ValidationError,
    ValidationResult,
    calculate_box_area,
    validate_annotation,
)
from labeling_service.area import calculate_box_area as module_calculate_box_area


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_example(category: str, name: str) -> dict[str, object]:
    path = REPOSITORY_ROOT / "examples" / category / name
    return json.loads(path.read_text(encoding="utf-8"))


def valid_annotation() -> dict[str, object]:
    return load_example("valid", "full_image.json")


class CalculateBoxAreaTests(unittest.TestCase):
    def test_public_import(self) -> None:
        self.assertIs(module_calculate_box_area, calculate_box_area)

    def test_calls_existing_validator_before_calculation(self) -> None:
        annotation: dict[str, object] = {
            "box": {
                "x_min": 10,
                "y_min": 20,
                "x_max": 30,
                "y_max": 50,
            }
        }

        with patch("labeling_service.area.validate_annotation") as validator:
            area = calculate_box_area(annotation)

        validator.assert_called_once_with(annotation)
        self.assertEqual(600, area)

    def test_full_frame_area(self) -> None:
        annotation = load_example("valid", "full_image.json")

        self.assertEqual(2073600, calculate_box_area(annotation))

    def test_lower_right_one_pixel_area(self) -> None:
        annotation = load_example("valid", "lower_right_pixel.json")

        self.assertEqual(1, calculate_box_area(annotation))

    def test_interior_box_area(self) -> None:
        annotation = valid_annotation()
        annotation["box"] = {
            "x_min": 10,
            "y_min": 20,
            "x_max": 30,
            "y_max": 50,
        }

        self.assertEqual(600, calculate_box_area(annotation))


class ValidationPropagationTests(unittest.TestCase):
    def test_propagates_same_validation_exception_instance(self) -> None:
        issue = ValidationError(code="INVALID_BOX", field="box")
        result = ValidationResult(accepted=False, errors=(issue,))
        expected = AnnotationValidationError(result)

        with patch(
            "labeling_service.area.validate_annotation",
            side_effect=expected,
        ):
            with self.assertRaises(AnnotationValidationError) as raised:
                calculate_box_area({})

        self.assertIs(expected, raised.exception)

    def test_invalid_examples_match_direct_validation(self) -> None:
        cases = {
            "geometry": load_example("invalid", "zero_width.json"),
            "provenance": load_example("invalid", "missing_provenance.json"),
            "ontology": load_example("invalid", "unknown_ontology.json"),
            "class": load_example("invalid", "unknown_class.json"),
            "closed_shape": load_example("invalid", "unknown_field.json"),
        }
        schema = valid_annotation()
        schema["schema_version"] = "2.0"
        cases["schema"] = schema
        coordinate_space = valid_annotation()
        coordinate_space["coordinate_space"] = "pixel_centers"
        cases["coordinate_space"] = coordinate_space

        for name, annotation in cases.items():
            with self.subTest(name=name):
                with self.assertRaises(AnnotationValidationError) as direct:
                    validate_annotation(annotation)
                with self.assertRaises(AnnotationValidationError) as helper:
                    calculate_box_area(annotation)

                self.assertEqual(direct.exception.code, helper.exception.code)
                self.assertEqual(direct.exception.errors, helper.exception.errors)
                self.assertEqual(direct.exception.result, helper.exception.result)

    def test_multiple_errors_keep_order_and_fields(self) -> None:
        annotation = load_example("invalid", "multiple_errors.json")

        with self.assertRaises(AnnotationValidationError) as direct:
            validate_annotation(annotation)
        with self.assertRaises(AnnotationValidationError) as helper:
            calculate_box_area(annotation)

        self.assertEqual(direct.exception.errors, helper.exception.errors)


class CompatibilityTests(unittest.TestCase):
    def test_does_not_mutate_annotation_or_add_area(self) -> None:
        annotation = valid_annotation()
        original = copy.deepcopy(annotation)

        calculate_box_area(annotation)

        self.assertEqual(original, annotation)
        self.assertNotIn("area", annotation)
        self.assertNotIn("area", annotation["box"])

    def test_does_not_mutate_invalid_annotation(self) -> None:
        annotation = load_example("invalid", "multiple_errors.json")
        original = copy.deepcopy(annotation)

        with self.assertRaises(AnnotationValidationError):
            calculate_box_area(annotation)

        self.assertEqual(original, annotation)
        self.assertNotIn("area", annotation)

    def test_repeated_calculation_is_deterministic(self) -> None:
        annotation = load_example("valid", "lower_right_pixel.json")
        original = copy.deepcopy(annotation)

        first = calculate_box_area(annotation)
        second = calculate_box_area(annotation)

        self.assertEqual(1, first)
        self.assertEqual(first, second)
        self.assertEqual(original, annotation)
