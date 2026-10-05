## Department constitution gate

- [x] The spec has approved, baseline-pinned requirements and measurable acceptance criteria.
- [x] Requirement-to-test traceability includes negative and boundary cases.
- [x] Data handling and least-privilege constraints have an accountable reviewer.
- [x] Architecture choices and assurance assumptions have human owners.
- [x] A sanitized session decision record and learning review are required in the future delivery tasks.
- [x] Conflicts and exception requests are resolved, not silently overridden.

No implementation task is blocked by the department gate. `/speckit-tasks` must
include the post-implementation ADAS capture and developer-review step.

# Implementation Plan: Validate Bounding Boxes

**Branch**: `001-validate-bounding-boxes` | **Date**: 2026-10-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-validate-bounding-boxes/spec.md`

## Summary

Create a small importable Python library that validates one synthetic annotation
mapping against the schema 1.0 half-open pixel-edge contract. The public
`validate_annotation` function returns an immutable successful result or raises a
named `AnnotationValidationError` carrying the complete deterministic rejected
result. Implementation will use Python 3.12-compatible standard-library features,
perform no I/O or mutation, and be verified with `unittest` plus synthetic JSON
examples.

## Technical Context

**Language/Version**: Python 3.12-compatible

**Primary Dependencies**: Python standard library only

**Storage**: N/A; validation is pure and stateless

**Testing**: `unittest` with `unittest.mock` only if mutation detection requires it

**Target Platform**: CPython 3.12 on Windows for the demo; platform-neutral library behavior

**Project Type**: Importable Python library

**Performance Goals**: No requirement-owner performance target exists; correctness and deterministic results take precedence

**Constraints**: No input mutation, clipping, rounding, coercion, I/O, network access, persistence, web framework, or added dependency

**Scale/Scope**: One annotation containing one bounding box per function call; synthetic examples only

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Gate | Pre-design | Post-design evidence |
|------|------------|----------------------|
| Approved, pinned requirements | PASS | ADAS-LBL-001@3, ADAS-LBL-002@2, and ADAS-LBL-003@1 remain approved at `DEMO-ADAS-2026.10`. |
| Current-revision drift | PASS | `CURRENT` returned the same revisions and approved statuses on 2026-10-05; the pinned baseline remains unchanged. |
| Explicit annotation contract | PASS | [data-model.md](./data-model.md) and [validation.md](./contracts/validation.md) preserve pixel-edge units, orientation assumptions, schema, ontology, and provenance. |
| Negative and boundary evidence | PASS | The mapping below covers exact edges, one-pixel boxes, types, geometry, provenance, ontology, class, closed shape, and non-mutation. |
| Data minimization | PASS | Examples are synthetic metadata; the library reads no imagery and performs no storage or transport. |
| Human ownership | PASS | Labeling service team owns implementation evidence; Requirements Engineering and the ADAS data architecture council retain their stated ownership. |
| Deferred requirement behavior | PASS | Revision history and dataset-release gating remain deferred and are not represented as validator behavior. |
| Exceptions or conflicts | PASS | No policy exception or requirements conflict is present. |

## Requirement Drift Review

Read-only DOORS checks compared the pinned baseline with `CURRENT`:

| Requirement | Pinned | Current | Decision |
|-------------|--------|---------|----------|
| ADAS-LBL-001 | Revision 3, approved | Revision 3, approved | No drift; continue with pinned revision 3. |
| ADAS-LBL-002 | Revision 2, approved | Revision 2, approved | No drift; continue with pinned revision 2 and retain explicit deferrals. |
| ADAS-LBL-003 | Revision 1, approved | Revision 1, approved | No drift; continue with pinned revision 1. |

## Public Interface Design

- `labeling_service.__init__` re-exports `validate_annotation`,
  `AnnotationValidationError`, `ValidationError`, and `ValidationResult`.
- `validate_annotation(annotation)` accepts the closed mapping shape documented in
  [validation.md](./contracts/validation.md).
- Valid input returns `ValidationResult(accepted=True, errors=())`.
- Invalid input raises `AnnotationValidationError`. The exception has stable code
  `ANNOTATION_VALIDATION_FAILED` and exposes
  `ValidationResult(accepted=False, errors=(...))`.
- Every `ValidationError` contains only stable `code` and `field` strings.
- Frozen data values prevent callers from mutating validation evidence.
- Validation observes but never modifies the supplied mapping or nested box.

## Validation Sequence

1. Detect unknown top-level fields and validate independent envelope fields.
2. Validate that `box` is an object; `INVALID_BOX` suppresses dependent box checks.
3. Detect unknown box fields and validate each required coordinate type.
4. Run zero-area, reversed-edge, and bounds checks only when dimensions and all
   coordinates are valid integers excluding booleans.
5. Deduplicate `(code, field)` pairs and sort by the specification's code order,
   then known field order; sort unknown paths lexically.
6. Return the successful result or raise the named exception with the complete
   rejected result. Verify deep equality of input before and after both paths.

## Project Structure

### Documentation (this feature)

```text
specs/001-validate-bounding-boxes/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── validation.md
└── tasks.md                 # Created later by /speckit-tasks
```

### Source Code (repository root)

```text
labeling_service/
├── __init__.py
└── validation.py

tests/
└── test_validation.py

examples/
├── valid/
│   ├── full_image.json
│   └── lower_right_pixel.json
└── invalid/
    ├── boolean_coordinate.json
    ├── fractional_coordinate.json
    ├── missing_provenance.json
    ├── multiple_errors.json
    ├── unknown_class.json
    ├── unknown_field.json
    ├── unknown_ontology.json
    └── zero_width.json
```

**Structure Decision**: Use a root-level package so it is directly importable
from the repository without packaging dependencies. Keep all validation behavior
in one focused module, all tests in one `unittest` module, and synthetic examples
separate from tests so reviewers can inspect contract cases without executing code.

## Requirement-to-Test Mapping

Planned test names are defined before implementation and may be grouped into
`unittest.TestCase` classes without changing their trace meaning.

| Source criterion | Coverage status | Planned test evidence |
|------------------|-----------------|-----------------------|
| ADAS-LBL-001@3: positive dimensions and half-open inequalities | In scope | `test_accepts_valid_interior_box`, `test_rejects_zero_area`, `test_rejects_reversed_edges`, `test_rejects_each_out_of_bounds_edge` |
| ADAS-LBL-001@3: complete frame and right/bottom one-pixel box | In scope | `test_accepts_complete_frame`, `test_accepts_lower_right_one_pixel_box` |
| ADAS-LBL-001@3: reject booleans, fractions, invalid geometry, and range | In scope | `test_rejects_boolean_coordinate`, `test_rejects_fractional_coordinate`, `test_rejects_zero_area`, `test_rejects_reversed_edges`, `test_rejects_each_out_of_bounds_edge` |
| ADAS-LBL-001@3: schema 1.0, pixel edges, no conversion | In scope | `test_rejects_unsupported_schema`, `test_rejects_unsupported_coordinate_space`, `test_does_not_mutate_valid_input`, `test_does_not_mutate_invalid_input` |
| ADAS-LBL-002@2: frame ID, dimensions, annotation revision | In scope | `test_rejects_missing_frame_id`, `test_rejects_invalid_frame_dimensions`, `test_rejects_invalid_annotation_revision` |
| ADAS-LBL-002@2: correction creates linked revision | Deferred | No validator test; separate revision-history feature required. |
| ADAS-LBL-002@2: reviewed-only approved datasets | Deferred | No validator test; separate review and dataset-release feature required. |
| ADAS-LBL-003@1: required ontology | In scope | `test_rejects_missing_or_unsupported_ontology` |
| ADAS-LBL-003@1: allowed and unknown classes | In scope | `test_accepts_each_allowed_class`, `test_rejects_missing_or_unknown_class` |
| Clarified closed input shape | Approved local clarification | `test_rejects_unknown_top_level_field`, `test_rejects_unknown_box_field`, `test_rejects_missing_or_non_object_box` |
| Clarified aggregate error contract | Approved local clarification | `test_returns_all_errors_in_stable_order`, `test_deduplicates_code_field_pairs`, `test_omits_dependent_geometry_errors` |
| Public exception contract | Plan-level interface choice | `test_invalid_annotation_raises_named_exception`, `test_exception_has_stable_code_and_rejected_result` |
| Synthetic example contract | User-requested plan scope | `test_all_valid_examples_pass`, `test_all_invalid_examples_raise_validation_error` |

## Phase Outputs

- Phase 0 decisions: [research.md](./research.md)
- Phase 1 entity and validation model: [data-model.md](./data-model.md)
- Phase 1 public library contract: [validation.md](./contracts/validation.md)
- Phase 1 runnable validation guide: [quickstart.md](./quickstart.md)

## ADAS integration gate

- [x] Shared contracts and explicit units match the product ADRs.
- [x] Frame, annotation, ontology and dataset lineage is preserved.
- [x] Boundary tests include exact image edges, non-integers and unknown classes.
- [x] Downstream dataset/training/evaluation impacts and human review are covered.
- [x] No autonomous-driving deployment or certification claim is inferred.

The post-design gate passes. No complexity exception is required.
