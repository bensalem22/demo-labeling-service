# Phase 0 Research: Validate Bounding Boxes

No unresolved `NEEDS CLARIFICATION` item remains. Decisions below record the
user-selected stack and the smallest design that satisfies the specification.

## Python library shape

**Decision**: Use a root-level `labeling_service` package compatible with Python
3.12 and export the public interface from `labeling_service.__init__`.

**Rationale**: The repository has no existing application package or build
configuration. A root-level package is directly importable during local tests and
requires no packaging dependency or unrelated project scaffolding.

**Alternatives considered**:

- `src/labeling_service`: rejected for this small demo because it would require
  packaging or test-path configuration not requested by the feature.
- A script or CLI: rejected because the requested interface is importable and no
  command-line behavior is in scope.
- A web service: explicitly out of scope.

## Standard-library data contracts

**Decision**: Represent immutable validation evidence with frozen data values in
`validation.py`, while accepting the annotation as a read-only mapping shape.

**Rationale**: Frozen result and error values preserve stable evidence without
mutating caller input. Mapping input matches the synthetic JSON examples and keeps
the library independent of transport or persistence models.

**Alternatives considered**:

- Third-party schema or validation packages: rejected by the no-dependency
  constraint.
- Mutable dictionaries as results: rejected because they weaken evidence
  immutability and make accidental contract changes easier.
- Converting the annotation into a new domain object: rejected because the
  validator must not silently convert input.

## Invalid-result signaling

**Decision**: Return `ValidationResult(accepted=True, errors=())` for valid input.
For invalid input, raise `AnnotationValidationError` with stable exception code
`ANNOTATION_VALIDATION_FAILED` and attach the exact rejected
`ValidationResult(accepted=False, errors=(...))`.

**Rationale**: This satisfies both the clarified aggregate result contract and the
requested named validation exception. Callers can catch one public exception and
inspect every stable `(code, field)` error without parsing prose.

**Alternatives considered**:

- Return rejected results without raising: rejected because the plan explicitly
  requires a named validation exception.
- Raise one exception per detected defect: rejected because it would violate the
  clarified all-errors contract.
- Put human-readable messages in errors: rejected because the clarified contract
  permits only code and field.

## Validation ordering

**Decision**: Validate independent envelope and shape rules first; run geometry
comparisons only when both dimensions and all coordinates are valid integers.
Deduplicate code/field pairs and sort by the specification's code and field order.

**Rationale**: This produces deterministic evidence and avoids speculative
geometry errors when comparison prerequisites are invalid.

**Alternatives considered**:

- Fail fast: rejected by the clarification requiring all detected errors.
- Best-effort comparisons with invalid values: rejected because they can generate
  misleading or runtime-dependent errors.

## Testing and examples

**Decision**: Use `unittest` and synthetic JSON files under `examples/valid` and
`examples/invalid`. Keep focused contract tests in `tests/test_validation.py`.

**Rationale**: `unittest` and `json` are standard-library modules, require no
dependency changes, and can verify both direct cases and inspectable examples.

**Alternatives considered**:

- `pytest`: rejected because adding dependencies is prohibited.
- Generated or production-derived imagery: rejected because only synthetic
  metadata is required and production data is prohibited.

## Requirements drift

**Decision**: Continue using baseline `DEMO-ADAS-2026.10`.

**Rationale**: The 2026-10-05 plan-time `CURRENT` check returned
ADAS-LBL-001@3, ADAS-LBL-002@2, and ADAS-LBL-003@1 with approved status, exactly
matching the pinned baseline. No impact-analysis block is required.

**Alternatives considered**: None; no changed revision or status was returned.
