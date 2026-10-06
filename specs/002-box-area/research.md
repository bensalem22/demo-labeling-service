# Phase 0 Research: Calculate Box Area

No unresolved `NEEDS CLARIFICATION` item remains. The existing package and the
approved specification determine a small additive design.

## Module placement

**Decision**: Add `labeling_service/area.py` and re-export
`calculate_box_area` from the existing package.

**Rationale**: A separate module keeps derived calculations out of the shared
validator, makes the change easy to review, and preserves the existing public
validation implementation.

**Alternatives considered**:

- Add the helper to `validation.py`: not selected because area is derived output,
  not a validation rule, and the existing validator should remain unchanged.
- Create a new package: rejected as unnecessary duplication for one helper.
- Add a CLI or web endpoint: explicitly outside scope.

## Validation reuse and error propagation

**Decision**: Call `validate_annotation(annotation)` directly and do not catch its
exception before reading coordinates.

**Rationale**: Direct delegation guarantees all current and future validator rules
run once and naturally propagates the exact `AnnotationValidationError` instance,
stable code, ordered errors, and rejected result.

**Alternatives considered**:

- Recheck coordinate and metadata rules in the helper: rejected because it
  duplicates governed validation logic and can drift.
- Catch and reconstruct the validation exception: rejected because it changes
  exception identity and risks changing error evidence.
- Return a fallback area: prohibited by the local requirement.

## Area representation

**Decision**: Return a Python integer calculated as
`(x_max - x_min) * (y_max - y_min)` after validation.

**Rationale**: ADR-0001 coordinates and extents are integers, accepted boxes have
positive width and height, and Python integers preserve the exact square-pixel
result without rounding or overflow conversion.

**Alternatives considered**:

- Inclusive `+1` extents: rejected because endpoints are half-open pixel edges.
- Floating-point area: rejected because it weakens the integer contract.
- Persisted or envelope area field: rejected because it changes the shared schema
  and lineage.

## Testing

**Decision**: Add `tests/test_box_area.py`, reuse existing synthetic examples, and
run the full existing `unittest` discovery command.

**Rationale**: A focused module keeps helper tests separate while the full suite
proves the validator remains unchanged. Standard-library mocking can verify exact
exception-object propagation without adding a dependency.

**Alternatives considered**:

- Modify `tests/test_validation.py`: not selected because helper behavior can be
  tested independently and existing regression tests should remain unchanged.
- Add new third-party test tools: prohibited by the no-dependency constraint.

## Requirement drift

**Decision**: Continue with `DEMO-ADAS-2026.10` and the approved local requirement.

**Rationale**: Plan-time `CURRENT` returned ADAS-LBL-001@3,
ADAS-LBL-002@2, and ADAS-LBL-003@1 with approved status, matching the pinned
baseline. `LOCAL-LBL-DEMO-001@1` retains its recorded service-owner provenance.

**Alternatives considered**: None; no revision or status drift was returned.
