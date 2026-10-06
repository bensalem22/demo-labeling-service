## Department constitution gate

- [x] The spec has approved, baseline-pinned requirements and measurable acceptance criteria.
- [x] Requirement-to-test traceability includes negative and boundary cases.
- [x] Data handling and least-privilege constraints have an accountable reviewer.
- [x] Architecture choices and assurance assumptions have human owners.
- [x] A sanitized session decision record and learning review are required in future delivery tasks.
- [x] Conflicts and exception requests are resolved, not silently overridden.

No implementation task is blocked by the department gate. The future task list
must include the mandatory ADAS capture and developer review.

# Implementation Plan: Calculate Box Area

**Branch**: `002-box-area` | **Date**: 2026-10-05 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-box-area/spec.md`

## Summary

Add one public `calculate_box_area(annotation)` helper to the existing Python
package. The helper delegates complete input validation to the existing
`validate_annotation` function, then calculates the half-open area from the
already validated box. A separate focused `unittest` module verifies exact areas,
unchanged exception propagation, input immutability, public import, and full
regression compatibility. No validation rule, annotation field, dependency, or
framework is added.

## Technical Context

**Language/Version**: Existing Python 3.12-compatible code

**Primary Dependencies**: Existing Python standard-library package only; no new dependency

**Storage**: N/A; calculation is pure and stateless

**Testing**: Existing `unittest` setup plus focused `tests/test_box_area.py`

**Target Platform**: Existing platform-neutral Python package; validated with the repository Windows virtual environment

**Project Type**: Importable Python library

**Performance Goals**: No requirement-owner target; one validator call plus constant-time integer arithmetic

**Constraints**: Reuse `validate_annotation`; do not duplicate validation logic, mutate input, change `validation.py`, add schema fields, catch/translate validation errors, or add dependencies

**Scale/Scope**: One annotation containing one box per helper invocation

## Constitution Check

*GATE: Passed before Phase 0 and re-checked after Phase 1 design.*

| Gate | Pre-design | Post-design evidence |
|------|------------|----------------------|
| Approved requirements | PASS | `LOCAL-LBL-DEMO-001@1` has direct service-owner approval; ADAS-LBL-001@3, ADAS-LBL-002@2, and ADAS-LBL-003@1 remain pinned and approved. |
| Current-revision drift | PASS | Plan-time `CURRENT` returned the same revisions and approved statuses as the pinned baseline. |
| Shared contract preservation | PASS | [data-model.md](./data-model.md) adds only a returned derived value; [box-area.md](./contracts/box-area.md) leaves schema 1.0 and validator behavior unchanged. |
| Explicit units and boundaries | PASS | Exact complete-frame, lower-right one-pixel, and interior area tests use ADR-0001 half-open square pixels. |
| Failure behavior | PASS | The helper delegates validation and does not catch or translate `AnnotationValidationError`. |
| Data minimization | PASS | Existing synthetic mappings are reused; no imagery, storage, transport, or telemetry is added. |
| Deferred ADAS-LBL-002 behavior | PASS | Revision history, review state, and dataset release remain outside the helper. |
| Exceptions or conflicts | PASS | No policy exception or requirement conflict exists. |

## Requirement Drift Review

| Requirement | Pinned | Current | Decision |
|-------------|--------|---------|----------|
| ADAS-LBL-001 | Revision 3, approved | Revision 3, approved | No drift; retain revision 3. |
| ADAS-LBL-002 | Revision 2, approved | Revision 2, approved | No drift; retain revision 2 and existing deferrals. |
| ADAS-LBL-003 | Revision 1, approved | Revision 1, approved | No drift; retain revision 1. |

The service-local `LOCAL-LBL-DEMO-001@1` approval remains pinned to the provenance
recorded in [spec.md](./spec.md); it is not queried through DOORS.

## Design

### Public helper

- Add `labeling_service/area.py` with
  `calculate_box_area(annotation: Mapping[str, object]) -> int`.
- Call `validate_annotation(annotation)` before reading `annotation["box"]`.
- Do not catch `AnnotationValidationError`; the same exception instance and
  existing result/error values propagate to the caller.
- After successful validation, return
  `(x_max - x_min) * (y_max - y_min)` with no `+1`.
- Re-export `calculate_box_area` from `labeling_service/__init__.py`.
- Do not modify `labeling_service/validation.py` or the annotation mapping.

### Focused tests

- Add `tests/test_box_area.py`; leave `tests/test_validation.py` unchanged.
- Reuse existing synthetic JSON examples for complete-frame, lower-right
  one-pixel, geometry, provenance, ontology, class, and closed-shape scenarios.
- Add one local valid `(10, 20, 30, 50)` annotation for the `600` example.
- Use `unittest.mock` only to prove the helper re-raises the exact validation
  exception object without translation.
- Run the full existing discovery command after focused tests.

### Public example

Add a short `README.md` example that loads the existing synthetic complete-frame
JSON file, imports `calculate_box_area`, and prints `2073600`. Keep full validation
rules in the existing contract documentation rather than duplicating them.

## Project Structure

### Documentation (this feature)

```text
specs/002-box-area/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── box-area.md
└── tasks.md                 # Created later by /speckit-tasks
```

### Source Code (repository root)

```text
labeling_service/
├── __init__.py              # Add public export
├── area.py                  # New helper only
└── validation.py            # Existing, unchanged

tests/
├── test_box_area.py         # New focused tests
└── test_validation.py       # Existing regression suite, unchanged

examples/
├── valid/                   # Existing synthetic inputs, reused
└── invalid/                 # Existing synthetic inputs, reused

README.md                    # Add short public API example
```

**Structure Decision**: Isolate the derived calculation in one new module and one
new test module. Re-export it through the existing package surface. This minimizes
changes and prevents area logic from becoming part of the shared validator or
annotation schema.

## Requirement-to-Test Mapping

| Source behavior | Planned evidence |
|-----------------|------------------|
| LOCAL-LBL-DEMO-001@1: validate first | `test_calls_existing_validator_before_calculation` |
| LOCAL-LBL-DEMO-001@1: half-open formula | `test_full_frame_area`, `test_lower_right_one_pixel_area`, `test_interior_box_area` |
| LOCAL-LBL-DEMO-001@1: propagate unchanged failures | `test_propagates_same_validation_exception_instance`, `test_invalid_examples_match_direct_validation` |
| LOCAL-LBL-DEMO-001@1: no input/schema mutation | `test_does_not_mutate_annotation_or_add_area` |
| ADAS-LBL-001@3: complete-frame and one-pixel endpoints | `test_full_frame_area`, `test_lower_right_one_pixel_area` |
| ADAS-LBL-001@3: invalid geometry and contract fields | `test_invalid_examples_match_direct_validation` plus unchanged `test_validation.py` |
| ADAS-LBL-002@2: required provenance | `test_invalid_examples_match_direct_validation` using `missing_provenance.json` |
| ADAS-LBL-002@2: revision history and reviewed datasets | Explicitly excluded; no helper behavior or test claims satisfaction. |
| ADAS-LBL-003@1: ontology and allowed classes | `test_invalid_examples_match_direct_validation` plus unchanged class/ontology regression tests |
| Existing public validator behavior | Full `unittest` discovery; all pre-existing tests must remain unchanged and pass. |
| Public import and example | `test_public_import` and the runnable [quickstart.md](./quickstart.md) command. |

## Phase Outputs

- Phase 0 decisions: [research.md](./research.md)
- Phase 1 derived-value model: [data-model.md](./data-model.md)
- Phase 1 public helper contract: [box-area.md](./contracts/box-area.md)
- Phase 1 validation guide: [quickstart.md](./quickstart.md)

## ADAS integration gate

- [x] Shared contracts and explicit units match the product ADRs.
- [x] Frame, annotation, ontology and dataset lineage is preserved.
- [x] Boundary tests include exact image edges, non-integers and unknown classes.
- [x] Downstream dataset/training/evaluation impacts and human review are covered.
- [x] No autonomous-driving deployment or certification claim is inferred.

The post-design gate passes. No complexity exception is required.
