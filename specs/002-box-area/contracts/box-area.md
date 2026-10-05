# Public Contract: Calculate Box Area

## Import surface

```python
from labeling_service import calculate_box_area
```

The existing validation imports and contracts remain unchanged.

## Function

```python
def calculate_box_area(annotation: Mapping[str, object]) -> int:
    ...
```

## Successful result

The function validates the complete annotation, then returns:

```text
(x_max - x_min) * (y_max - y_min)
```

The result is a positive integer in square pixels. No inclusive-endpoint `+1`
adjustment is applied.

| Valid box | Result |
|-----------|--------|
| `(0, 0, 1920, 1080)` | `2073600` |
| `(1919, 1079, 1920, 1080)` | `1` |
| `(10, 20, 30, 50)` | `600` |

## Invalid input

The helper calls the existing `validate_annotation` function and does not catch or
translate `AnnotationValidationError`. The same exception instance, stable code,
ordered code-and-field errors, and rejected result propagate unchanged. No area is
returned.

## Side effects

- The input mapping and nested box remain unchanged.
- No area or other field is added to the annotation.
- No data is stored, transmitted, logged, or persisted.
- No annotation revision, review state, or dataset state is created or changed.

## Compatibility

The helper is service-local under `LOCAL-LBL-DEMO-001@1`. It does not change
schema 1.0, ADR-0001, existing validator behavior, or existing public validation
imports. Any such change requires separate reviewed requirements and contract
updates.
