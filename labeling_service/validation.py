from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Final


ANNOTATION_FIELDS: Final[tuple[str, ...]] = (
    "frame_id",
    "frame_width",
    "frame_height",
    "annotation_revision",
    "schema_version",
    "coordinate_space",
    "ontology",
    "class_label",
    "box",
)
COORDINATE_FIELDS: Final[tuple[str, ...]] = (
    "x_min",
    "y_min",
    "x_max",
    "y_max",
)
ALLOWED_CLASSES: Final[frozenset[str]] = frozenset(
    {"car", "truck", "pedestrian", "cyclist"}
)
ERROR_CODE_ORDER: Final[tuple[str, ...]] = (
    "MISSING_FRAME_ID",
    "INVALID_FRAME_DIMENSIONS",
    "INVALID_ANNOTATION_REVISION",
    "UNSUPPORTED_SCHEMA_VERSION",
    "UNSUPPORTED_COORDINATE_SPACE",
    "INVALID_BOX",
    "INVALID_COORDINATE_TYPE",
    "ZERO_AREA_BOX",
    "REVERSED_BOX_EDGES",
    "BOX_OUT_OF_BOUNDS",
    "UNSUPPORTED_ONTOLOGY",
    "UNKNOWN_CLASS",
    "UNKNOWN_FIELD",
)
FIELD_ORDER: Final[tuple[str, ...]] = (
    "frame_id",
    "frame_width",
    "frame_height",
    "annotation_revision",
    "schema_version",
    "coordinate_space",
    "ontology",
    "class_label",
    "box",
    "box.x_min",
    "box.y_min",
    "box.x_max",
    "box.y_max",
)
_ERROR_RANK: Final = {code: index for index, code in enumerate(ERROR_CODE_ORDER)}
_FIELD_RANK: Final = {field: index for index, field in enumerate(FIELD_ORDER)}
_MISSING: Final = object()


@dataclass(frozen=True, slots=True)
class ValidationError:
    code: str
    field: str


@dataclass(frozen=True, slots=True)
class ValidationResult:
    accepted: bool
    errors: tuple[ValidationError, ...]

    def __post_init__(self) -> None:
        if self.accepted != (len(self.errors) == 0):
            raise ValueError("accepted must be true exactly when errors is empty")
        pairs = {(error.code, error.field) for error in self.errors}
        if len(pairs) != len(self.errors):
            raise ValueError("duplicate validation code and field pairs are not allowed")


class AnnotationValidationError(Exception):
    code = "ANNOTATION_VALIDATION_FAILED"

    def __init__(self, result: ValidationResult) -> None:
        if result.accepted or not result.errors:
            raise ValueError("annotation validation errors require a rejected result")
        self.result = result
        self.errors = result.errors
        super().__init__(self.code)


def _is_integer(value: object) -> bool:
    return type(value) is int


def _append_error(
    errors: list[ValidationError],
    code: str,
    field: str,
) -> None:
    errors.append(ValidationError(code=code, field=field))


def _ordered_unique_errors(
    errors: list[ValidationError],
) -> tuple[ValidationError, ...]:
    unique = {
        (error.code, error.field): error
        for error in errors
    }
    return tuple(
        sorted(
            unique.values(),
            key=lambda error: (
                _ERROR_RANK[error.code],
                _FIELD_RANK.get(error.field, len(_FIELD_RANK)),
                error.field,
            ),
        )
    )


def validate_annotation(annotation: Mapping[str, object]) -> ValidationResult:
    if not isinstance(annotation, Mapping):
        raise TypeError("annotation must be a mapping")

    errors: list[ValidationError] = []

    for field in annotation:
        if field not in ANNOTATION_FIELDS:
            _append_error(errors, "UNKNOWN_FIELD", str(field))

    frame_id = annotation.get("frame_id", _MISSING)
    if not isinstance(frame_id, str) or len(frame_id) == 0:
        _append_error(errors, "MISSING_FRAME_ID", "frame_id")

    frame_dimensions_valid = True
    dimensions: dict[str, int] = {}
    for field in ("frame_width", "frame_height"):
        value = annotation.get(field, _MISSING)
        if not _is_integer(value) or value <= 0:
            frame_dimensions_valid = False
            _append_error(errors, "INVALID_FRAME_DIMENSIONS", field)
        else:
            dimensions[field] = value

    annotation_revision = annotation.get("annotation_revision", _MISSING)
    if not _is_integer(annotation_revision) or annotation_revision <= 0:
        _append_error(
            errors,
            "INVALID_ANNOTATION_REVISION",
            "annotation_revision",
        )

    if annotation.get("schema_version", _MISSING) != "1.0":
        _append_error(errors, "UNSUPPORTED_SCHEMA_VERSION", "schema_version")

    if annotation.get("coordinate_space", _MISSING) != "pixel_edges":
        _append_error(
            errors,
            "UNSUPPORTED_COORDINATE_SPACE",
            "coordinate_space",
        )

    if annotation.get("ontology", _MISSING) != "DEMO-ROAD-USERS-1":
        _append_error(errors, "UNSUPPORTED_ONTOLOGY", "ontology")

    if annotation.get("class_label", _MISSING) not in ALLOWED_CLASSES:
        _append_error(errors, "UNKNOWN_CLASS", "class_label")

    box = annotation.get("box", _MISSING)
    if not isinstance(box, Mapping):
        _append_error(errors, "INVALID_BOX", "box")
    else:
        for field in box:
            if field not in COORDINATE_FIELDS:
                _append_error(errors, "UNKNOWN_FIELD", f"box.{field}")

        coordinates_valid = True
        coordinates: dict[str, int] = {}
        for field in COORDINATE_FIELDS:
            value = box.get(field, _MISSING)
            if not _is_integer(value):
                coordinates_valid = False
                _append_error(
                    errors,
                    "INVALID_COORDINATE_TYPE",
                    f"box.{field}",
                )
            else:
                coordinates[field] = value

        if frame_dimensions_valid and coordinates_valid:
            x_min = coordinates["x_min"]
            y_min = coordinates["y_min"]
            x_max = coordinates["x_max"]
            y_max = coordinates["y_max"]

            if x_min == x_max or y_min == y_max:
                _append_error(errors, "ZERO_AREA_BOX", "box")
            if x_min > x_max or y_min > y_max:
                _append_error(errors, "REVERSED_BOX_EDGES", "box")

            bounds = {
                "x_min": dimensions["frame_width"],
                "y_min": dimensions["frame_height"],
                "x_max": dimensions["frame_width"],
                "y_max": dimensions["frame_height"],
            }
            for field in COORDINATE_FIELDS:
                value = coordinates[field]
                if value < 0 or value > bounds[field]:
                    _append_error(
                        errors,
                        "BOX_OUT_OF_BOUNDS",
                        f"box.{field}",
                    )

    ordered_errors = _ordered_unique_errors(errors)
    if ordered_errors:
        result = ValidationResult(accepted=False, errors=ordered_errors)
        raise AnnotationValidationError(result)
    return ValidationResult(accepted=True, errors=())