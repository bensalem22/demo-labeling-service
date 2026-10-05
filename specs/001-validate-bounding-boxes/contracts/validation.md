# Public Contract: Annotation Validation

## Import surface

The `labeling_service` package exposes:

```python
from labeling_service import (
    AnnotationValidationError,
    ValidationError,
    ValidationResult,
    validate_annotation,
)
```

No transport, CLI, UI, database, or framework interface is part of this feature.

## Function

```python
def validate_annotation(annotation: Mapping[str, object]) -> ValidationResult:
    ...
```

The accepted mapping shape is defined in [data-model.md](../data-model.md).
The function observes the supplied mapping and nested box without changing either.

### Valid input

Returns an immutable result equivalent to:

```text
accepted = true
errors = ()
```

### Invalid input

Raises `AnnotationValidationError`:

```text
exception.code = "ANNOTATION_VALIDATION_FAILED"
exception.result.accepted = false
exception.result.errors = ordered detected errors
exception.errors = exception.result.errors
```

Each error contains exactly:

```text
code = one named validation code
field = one annotation field path
```

Exception prose is not stable contract data. Consumers use `code`, `field`, and
the rejected result instead of parsing the exception message.

## Stable validation codes

| Code | Field |
|------|-------|
| `MISSING_FRAME_ID` | `frame_id` |
| `INVALID_FRAME_DIMENSIONS` | `frame_width` or `frame_height` |
| `INVALID_ANNOTATION_REVISION` | `annotation_revision` |
| `UNSUPPORTED_SCHEMA_VERSION` | `schema_version` |
| `UNSUPPORTED_COORDINATE_SPACE` | `coordinate_space` |
| `INVALID_BOX` | `box` |
| `INVALID_COORDINATE_TYPE` | One of the four `box.*` coordinate paths |
| `ZERO_AREA_BOX` | `box` |
| `REVERSED_BOX_EDGES` | `box` |
| `BOX_OUT_OF_BOUNDS` | The offending `box.*` coordinate path |
| `UNSUPPORTED_ONTOLOGY` | `ontology` |
| `UNKNOWN_CLASS` | `class_label` |
| `UNKNOWN_FIELD` | The submitted unknown top-level or `box.*` path |

## Detection and ordering

1. Report all independently detectable errors.
2. Report each `(code, field)` pair once.
3. Sort by the code order above.
4. For repeated codes, sort known fields by annotation shape order.
5. Sort unknown paths lexically within `UNKNOWN_FIELD`.
6. If `box` is missing or is not a mapping, report `INVALID_BOX` and omit
   dependent coordinate, unknown-box-field, and geometry errors.
7. If any dimension or coordinate prerequisite is invalid, omit zero-area,
   reversed-edge, and bounds errors that cannot be evaluated reliably.

## Compatibility

The contract targets Python 3.12-compatible standard-library code. Changing the
annotation shape, public imports, exception code, validation codes, field paths,
or ordering rules is a contract change and requires reviewed specification and
test updates.
