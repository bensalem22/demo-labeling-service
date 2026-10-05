from __future__ import annotations

import copy
import json
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from labeling_service import (
    AnnotationValidationError,
    ValidationError,
    ValidationResult,
    validate_annotation,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def valid_annotation() -> dict[str, object]:
    return {
        "frame_id": "synthetic-frame-001",
        "frame_width": 1920,
        "frame_height": 1080,
        "annotation_revision": 1,
        "schema_version": "1.0",
        "coordinate_space": "pixel_edges",
        "ontology": "DEMO-ROAD-USERS-1",
        "class_label": "car",
        "box": {
            "x_min": 10,
            "y_min": 20,
            "x_max": 30,
            "y_max": 40,
        },
    }


def error_pairs(error: AnnotationValidationError) -> list[tuple[str, str]]:
    return [(item.code, item.field) for item in error.errors]


class PublicContractTests(unittest.TestCase):
    def test_validation_error_is_frozen(self) -> None:
        error = ValidationError(code="MISSING_FRAME_ID", field="frame_id")

        with self.assertRaises(FrozenInstanceError):
            error.code = "OTHER"  # type: ignore[misc]

    def test_validation_result_is_frozen_and_enforces_invariant(self) -> None:
        accepted = ValidationResult(accepted=True, errors=())
        issue = ValidationError(code="MISSING_FRAME_ID", field="frame_id")

        self.assertTrue(accepted.accepted)
        with self.assertRaises(FrozenInstanceError):
            accepted.accepted = False  # type: ignore[misc]
        with self.assertRaises(ValueError):
            ValidationResult(accepted=True, errors=(issue,))
        with self.assertRaises(ValueError):
            ValidationResult(accepted=False, errors=())

    def test_exception_has_stable_code_and_rejected_result(self) -> None:
        issue = ValidationError(code="MISSING_FRAME_ID", field="frame_id")
        result = ValidationResult(accepted=False, errors=(issue,))

        error = AnnotationValidationError(result)

        self.assertEqual("ANNOTATION_VALIDATION_FAILED", error.code)
        self.assertIs(result, error.result)
        self.assertEqual(result.errors, error.errors)

    def test_invalid_annotation_raises_named_exception(self) -> None:
        annotation = valid_annotation()
        annotation["frame_id"] = ""

        with self.assertRaises(AnnotationValidationError):
            validate_annotation(annotation)


class ValidAnnotationTests(unittest.TestCase):
    def test_accepts_valid_interior_box(self) -> None:
        result = validate_annotation(valid_annotation())

        self.assertEqual(ValidationResult(accepted=True, errors=()), result)

    def test_accepts_complete_frame(self) -> None:
        annotation = valid_annotation()
        annotation["box"] = {
            "x_min": 0,
            "y_min": 0,
            "x_max": 1920,
            "y_max": 1080,
        }

        self.assertTrue(validate_annotation(annotation).accepted)

    def test_accepts_lower_right_one_pixel_box(self) -> None:
        annotation = valid_annotation()
        annotation["box"] = {
            "x_min": 1919,
            "y_min": 1079,
            "x_max": 1920,
            "y_max": 1080,
        }

        self.assertTrue(validate_annotation(annotation).accepted)

    def test_does_not_mutate_valid_input(self) -> None:
        annotation = valid_annotation()
        original = copy.deepcopy(annotation)

        validate_annotation(annotation)

        self.assertEqual(original, annotation)


class GeometryRejectionTests(unittest.TestCase):
    def assert_rejected(
        self,
        annotation: dict[str, object],
        expected: list[tuple[str, str]],
    ) -> AnnotationValidationError:
        with self.assertRaises(AnnotationValidationError) as raised:
            validate_annotation(annotation)
        self.assertEqual(expected, error_pairs(raised.exception))
        return raised.exception

    def test_rejects_boolean_coordinate(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["x_min"] = False  # type: ignore[index]
        self.assert_rejected(
            annotation,
            [("INVALID_COORDINATE_TYPE", "box.x_min")],
        )

    def test_rejects_fractional_coordinate(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["x_max"] = 30.5  # type: ignore[index]
        self.assert_rejected(
            annotation,
            [("INVALID_COORDINATE_TYPE", "box.x_max")],
        )

    def test_rejects_numeric_text_coordinate(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["y_min"] = "20"  # type: ignore[index]
        self.assert_rejected(
            annotation,
            [("INVALID_COORDINATE_TYPE", "box.y_min")],
        )

    def test_rejects_missing_coordinate(self) -> None:
        annotation = valid_annotation()
        del annotation["box"]["y_max"]  # type: ignore[index]
        self.assert_rejected(
            annotation,
            [("INVALID_COORDINATE_TYPE", "box.y_max")],
        )

    def test_rejects_zero_width(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["x_max"] = 10  # type: ignore[index]
        self.assert_rejected(annotation, [("ZERO_AREA_BOX", "box")])

    def test_rejects_zero_height(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["y_max"] = 20  # type: ignore[index]
        self.assert_rejected(annotation, [("ZERO_AREA_BOX", "box")])

    def test_rejects_reversed_horizontal_edges(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["x_min"] = 31  # type: ignore[index]
        self.assert_rejected(annotation, [("REVERSED_BOX_EDGES", "box")])

    def test_rejects_reversed_vertical_edges(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["y_min"] = 41  # type: ignore[index]
        self.assert_rejected(annotation, [("REVERSED_BOX_EDGES", "box")])

    def test_rejects_each_negative_edge(self) -> None:
        for coordinate in ("x_min", "y_min", "x_max", "y_max"):
            with self.subTest(coordinate=coordinate):
                annotation = valid_annotation()
                annotation["box"][coordinate] = -1  # type: ignore[index]
                expected = [("BOX_OUT_OF_BOUNDS", f"box.{coordinate}")]
                if coordinate in ("x_max", "y_max"):
                    expected.insert(0, ("REVERSED_BOX_EDGES", "box"))
                self.assert_rejected(annotation, expected)

    def test_rejects_each_over_boundary_edge(self) -> None:
        values = {
            "x_min": 1921,
            "y_min": 1081,
            "x_max": 1921,
            "y_max": 1081,
        }
        for coordinate, value in values.items():
            with self.subTest(coordinate=coordinate):
                annotation = valid_annotation()
                annotation["box"][coordinate] = value  # type: ignore[index]
                expected = [("BOX_OUT_OF_BOUNDS", f"box.{coordinate}")]
                if coordinate in ("x_min", "y_min"):
                    expected.insert(0, ("REVERSED_BOX_EDGES", "box"))
                self.assert_rejected(annotation, expected)

    def test_does_not_mutate_invalid_input(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["x_min"] = 50  # type: ignore[index]
        original = copy.deepcopy(annotation)

        with self.assertRaises(AnnotationValidationError):
            validate_annotation(annotation)

        self.assertEqual(original, annotation)

    def test_returns_all_errors_in_stable_order(self) -> None:
        annotation = valid_annotation()
        annotation["frame_id"] = ""
        annotation["frame_width"] = False
        annotation["schema_version"] = "2.0"
        annotation["ontology"] = "UNKNOWN"
        annotation["class_label"] = "bus"
        annotation["extra_top"] = "unchanged"
        annotation["box"]["x_min"] = 1.5  # type: ignore[index]
        annotation["box"]["extra"] = 4  # type: ignore[index]

        self.assert_rejected(
            annotation,
            [
                ("MISSING_FRAME_ID", "frame_id"),
                ("INVALID_FRAME_DIMENSIONS", "frame_width"),
                ("UNSUPPORTED_SCHEMA_VERSION", "schema_version"),
                ("INVALID_COORDINATE_TYPE", "box.x_min"),
                ("UNSUPPORTED_ONTOLOGY", "ontology"),
                ("UNKNOWN_CLASS", "class_label"),
                ("UNKNOWN_FIELD", "box.extra"),
                ("UNKNOWN_FIELD", "extra_top"),
            ],
        )

    def test_deduplicates_code_field_pairs(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["x_min"] = -1  # type: ignore[index]

        with self.assertRaises(AnnotationValidationError) as raised:
            validate_annotation(annotation)

        pairs = error_pairs(raised.exception)
        self.assertEqual(len(pairs), len(set(pairs)))

    def test_omits_dependent_geometry_errors(self) -> None:
        annotation = valid_annotation()
        annotation["frame_width"] = False
        annotation["box"]["x_min"] = 100  # type: ignore[index]
        annotation["box"]["x_max"] = 10  # type: ignore[index]

        self.assert_rejected(
            annotation,
            [("INVALID_FRAME_DIMENSIONS", "frame_width")],
        )


class MetadataRejectionTests(unittest.TestCase):
    def assert_single_error(
        self,
        annotation: dict[str, object],
        code: str,
        field: str,
    ) -> None:
        with self.assertRaises(AnnotationValidationError) as raised:
            validate_annotation(annotation)
        self.assertEqual([(code, field)], error_pairs(raised.exception))

    def test_rejects_missing_empty_and_non_string_frame_id(self) -> None:
        for value in (None, "", 42):
            with self.subTest(value=value):
                annotation = valid_annotation()
                if value is None:
                    del annotation["frame_id"]
                else:
                    annotation["frame_id"] = value
                self.assert_single_error(
                    annotation,
                    "MISSING_FRAME_ID",
                    "frame_id",
                )

    def test_preserves_nonempty_frame_id_without_trimming(self) -> None:
        annotation = valid_annotation()
        annotation["frame_id"] = " "

        self.assertTrue(validate_annotation(annotation).accepted)
        self.assertEqual(" ", annotation["frame_id"])

    def test_rejects_invalid_frame_dimensions(self) -> None:
        invalid_values = (None, "1920", True, 1.5, 0, -1)
        for field in ("frame_width", "frame_height"):
            for value in invalid_values:
                with self.subTest(field=field, value=value):
                    annotation = valid_annotation()
                    if value is None:
                        del annotation[field]
                    else:
                        annotation[field] = value
                    self.assert_single_error(
                        annotation,
                        "INVALID_FRAME_DIMENSIONS",
                        field,
                    )

    def test_rejects_invalid_annotation_revision(self) -> None:
        for value in (None, "1", True, 1.5, 0, -1):
            with self.subTest(value=value):
                annotation = valid_annotation()
                if value is None:
                    del annotation["annotation_revision"]
                else:
                    annotation["annotation_revision"] = value
                self.assert_single_error(
                    annotation,
                    "INVALID_ANNOTATION_REVISION",
                    "annotation_revision",
                )

    def test_rejects_unsupported_schema(self) -> None:
        for value in (None, "2.0", 1.0):
            with self.subTest(value=value):
                annotation = valid_annotation()
                if value is None:
                    del annotation["schema_version"]
                else:
                    annotation["schema_version"] = value
                self.assert_single_error(
                    annotation,
                    "UNSUPPORTED_SCHEMA_VERSION",
                    "schema_version",
                )

    def test_rejects_unsupported_coordinate_space(self) -> None:
        for value in (None, "inclusive_pixels"):
            with self.subTest(value=value):
                annotation = valid_annotation()
                if value is None:
                    del annotation["coordinate_space"]
                else:
                    annotation["coordinate_space"] = value
                self.assert_single_error(
                    annotation,
                    "UNSUPPORTED_COORDINATE_SPACE",
                    "coordinate_space",
                )

    def test_rejects_missing_or_unsupported_ontology(self) -> None:
        for value in (None, "OTHER-ONTOLOGY"):
            with self.subTest(value=value):
                annotation = valid_annotation()
                if value is None:
                    del annotation["ontology"]
                else:
                    annotation["ontology"] = value
                self.assert_single_error(
                    annotation,
                    "UNSUPPORTED_ONTOLOGY",
                    "ontology",
                )

    def test_accepts_each_allowed_class(self) -> None:
        for class_label in ("car", "truck", "pedestrian", "cyclist"):
            with self.subTest(class_label=class_label):
                annotation = valid_annotation()
                annotation["class_label"] = class_label
                self.assertTrue(validate_annotation(annotation).accepted)

    def test_rejects_missing_or_unknown_class(self) -> None:
        for value in (None, "bus"):
            with self.subTest(value=value):
                annotation = valid_annotation()
                if value is None:
                    del annotation["class_label"]
                else:
                    annotation["class_label"] = value
                self.assert_single_error(annotation, "UNKNOWN_CLASS", "class_label")

    def test_rejects_unknown_top_level_field(self) -> None:
        annotation = valid_annotation()
        annotation["unexpected"] = "unchanged"
        self.assert_single_error(annotation, "UNKNOWN_FIELD", "unexpected")

    def test_rejects_unknown_box_field(self) -> None:
        annotation = valid_annotation()
        annotation["box"]["score"] = 0.9  # type: ignore[index]
        self.assert_single_error(annotation, "UNKNOWN_FIELD", "box.score")

    def test_rejects_missing_or_non_object_box(self) -> None:
        for value in (None, [], "box"):
            with self.subTest(value=value):
                annotation = valid_annotation()
                if value is None:
                    del annotation["box"]
                else:
                    annotation["box"] = value
                self.assert_single_error(annotation, "INVALID_BOX", "box")

    def test_invalid_box_suppresses_dependent_errors(self) -> None:
        annotation = valid_annotation()
        annotation["box"] = ["x_min", "extra"]
        self.assert_single_error(annotation, "INVALID_BOX", "box")


class SyntheticExampleTests(unittest.TestCase):
    def test_all_valid_examples_pass(self) -> None:
        for path in sorted((REPOSITORY_ROOT / "examples" / "valid").glob("*.json")):
            with self.subTest(path=path.name):
                annotation = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(validate_annotation(annotation).accepted)

    def test_all_invalid_examples_raise_validation_error(self) -> None:
        paths = sorted((REPOSITORY_ROOT / "examples" / "invalid").glob("*.json"))
        self.assertGreater(len(paths), 0)
        for path in paths:
            with self.subTest(path=path.name):
                annotation = json.loads(path.read_text(encoding="utf-8"))
                with self.assertRaises(AnnotationValidationError):
                    validate_annotation(annotation)


if __name__ == "__main__":
    unittest.main()
