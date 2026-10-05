---

description: "Test-first task list for the validated box-area helper"
---

# Tasks: Calculate Box Area

**Input**: Design documents from `specs/002-box-area/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/box-area.md`, `quickstart.md`

**Tests**: Required. Create the complete focused `unittest` contract suite and
observe its expected missing-helper failure before changing application code.

**Organization**: The shared test-first phase establishes evidence for all three
stories before implementation. Story phases then implement the one shared helper
and verify each independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it changes a different file or only reads
  completed behavior.
- **[Story]**: Maps the task to a specification user story.
- Every task names the file it creates, changes, or validates.

## Phase 1: Setup and Baseline

**Purpose**: Confirm the existing validator baseline before any feature change.

- [X] T001 Run `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` against `tests/test_validation.py` before editing application code, record the exact baseline count and outcomes for later comparison, and stop feature work if the existing suite is not green

**Checkpoint**: Existing validator behavior has an observed, passing baseline.

---

## Phase 2: Foundational Test-First Contract

**Purpose**: Encode all approved helper behavior before implementation.

**CRITICAL**: Complete this phase and observe the expected red result before
creating `labeling_service/area.py` or changing package exports.

- [X] T002 Create `tests/test_box_area.py` using only `unittest`, `unittest.mock`, `copy`, `json`, and `pathlib`; define focused `CalculateBoxAreaTests`, `ValidationPropagationTests`, and `CompatibilityTests` covering public import, validator-first execution, exact full-frame `2073600`, lower-right one-pixel `1`, interior `(10, 20, 30, 50)` result `600`, no inclusive `+1`, exact exception-instance propagation through a validator mock, direct-validator equivalence for representative invalid geometry/provenance/schema/coordinate-space/ontology/class/closed-shape inputs, stable ordered code-and-field errors, valid and invalid deep input equality with no added `area` field, and deterministic repeated calculation; reuse `examples/valid/full_image.json`, `examples/valid/lower_right_pixel.json`, and existing `examples/invalid/*.json`, deriving missing representative invalid variants in the test without changing submitted values
- [X] T003 Run `.\.venv\Scripts\python.exe -m unittest -v tests.test_box_area` against `tests/test_box_area.py` before implementation and record the expected failure caused by the missing `calculate_box_area` public helper; do not weaken assertions or add a success-shaped stub

**Checkpoint**: The complete approved helper contract is executable and red for
the expected missing behavior.

---

## Phase 3: User Story 1 - Calculate Validated Box Area (Priority: P1) MVP

**Goal**: Return exact square-pixel areas for contract-valid half-open boxes.

**Independent Test**: The complete-frame, lower-right one-pixel, and interior
examples return `2073600`, `1`, and `600`, the validator runs first, and the public
package import succeeds.

### Implementation

- [X] T004 [US1] Create `labeling_service/area.py` with Python 3.12-compatible `calculate_box_area(annotation: Mapping[str, object]) -> int`; call the existing `validate_annotation(annotation)` before reading `annotation["box"]`, then return exactly `(x_max - x_min) * (y_max - y_min)` with no `+1`, copied validation rules, input writes, fallback value, persistence, transport, or new dependency
- [X] T005 [US1] Re-export `calculate_box_area` from `labeling_service/__init__.py` without changing or removing any existing public validation export
- [X] T006 [US1] Run `.\.venv\Scripts\python.exe -m unittest -v tests.test_box_area.CalculateBoxAreaTests` against `tests/test_box_area.py`, load both existing files under `examples/valid/`, and confirm the public import, validator-first call, and exact `2073600`, `1`, and `600` results pass

**Checkpoint**: User Story 1 is independently usable as the MVP.

---

## Phase 4: User Story 2 - Preserve Validation Failures (Priority: P1)

**Goal**: Invalid annotations fail through the existing validator without
translation or partial area output.

**Independent Test**: Representative invalid inputs produce the same stable
exception code, ordered code-and-field errors, and rejected result as direct
validation, while a mocked validator exception propagates as the exact same
object.

### Verification

- [X] T007 [P] [US2] Run `.\.venv\Scripts\python.exe -m unittest -v tests.test_box_area.ValidationPropagationTests` against `tests/test_box_area.py`; verify invalid geometry, missing provenance, unsupported schema and coordinate space, unknown ontology and class, and closed-shape violations return no area and preserve the existing `AnnotationValidationError` instance or direct-validation evidence without any catch/translate logic in `labeling_service/area.py`

**Checkpoint**: User Story 2 proves the helper cannot bypass or reinterpret the
governed validator.

---

## Phase 5: User Story 3 - Preserve Annotation and Validator Compatibility (Priority: P2)

**Goal**: Keep caller input, schema 1.0, public validation behavior, and existing
evidence unchanged.

**Independent Test**: Valid and invalid inputs remain deeply equal with no `area`
field, repeated calls are deterministic, and all pre-existing validator tests pass
without modification.

### Verification and documentation

- [X] T008 [P] [US3] Run `.\.venv\Scripts\python.exe -m unittest -v tests.test_box_area.CompatibilityTests` against `tests/test_box_area.py` and confirm every valid and invalid case preserves deep input equality, adds no field to the annotation or nested box, and returns the same area on repeated valid calls
- [X] T009 [P] [US3] Add a short public API example to `README.md` that imports `calculate_box_area`, loads the synthetic `examples/valid/full_image.json`, prints `2073600`, states that validation errors propagate unchanged, and links to `specs/002-box-area/contracts/box-area.md` and `specs/002-box-area/quickstart.md` without duplicating validation rules

**Checkpoint**: User Story 3 preserves the annotation contract and documents the
new service-local helper.

---

## Phase 6: Regression, Traceability, and Reviewed Session Capture

**Purpose**: Produce final reproducible evidence and the mandatory sanitized,
human-reviewed learning record.

- [X] T010 Run the focused command from `specs/002-box-area/quickstart.md`, `.\.venv\Scripts\python.exe -m unittest -v tests.test_box_area`, and record the exact final focused test count and outcomes; resolve any feature-caused failure without weakening `tests/test_box_area.py` or changing governed contracts
- [X] T011 Run the full regression command from `specs/002-box-area/quickstart.md`, `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`, compare its existing-validator results with the T001 baseline, record the exact total count, failures, and errors, and resolve every feature-caused regression without modifying `tests/test_validation.py` or `labeling_service/validation.py`
- [X] T012 Run the short public API example from `specs/002-box-area/quickstart.md` with `.\.venv\Scripts\python.exe`, confirm it imports through `labeling_service/__init__.py` and prints exactly `2073600`, and record the observed output rather than an assumed result
- [X] T013 Review `specs/002-box-area/spec.md`, `specs/002-box-area/plan.md`, `labeling_service/area.py`, and `tests/test_box_area.py` for final traceability: link `LOCAL-LBL-DEMO-001@1` to the helper tests, preserve ADAS-LBL-001@3, ADAS-LBL-002@2, ADAS-LBL-003@1 and ADR-0001 reuse evidence, and do not claim the deferred revision-history or dataset-release behaviors are satisfied
- [X] T014 Execute the mandatory `/speckit-adas-capture` after T010-T013 and verify it creates `docs/session-notes/002-box-area.json` containing only a concise sanitized decision summary, actual commands and observed outcomes, requirement revisions, the validator-reuse and no-`+1` decisions, rejected alternatives, limitations, and `"approved_for_sharing": false`; include no raw transcript, credentials, private reasoning, invented approval, incident, failed attempt, or production data
- [X] T015 Require a developer to review and redact `docs/session-notes/002-box-area.json`, verify every recorded test outcome against T010-T012, and explicitly approve that exact shareable record or leave `"approved_for_sharing": false`; the implementing agent MUST NOT approve its own proposal, infer approval, or promote a lesson into service, product, or department policy

**Checkpoint**: The feature has focused, regression, quickstart, traceability, and
developer-reviewed session evidence.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup and Baseline)**: No dependencies; must pass before edits.
- **Phase 2 (Test-First Contract)**: Depends on T001 and blocks implementation.
- **User Story 1 (Phase 3)**: Depends on the expected red result in T003.
- **User Story 2 (Phase 4)**: Depends on T004-T005 because it verifies the shared
  helper, but has no additional implementation dependency.
- **User Story 3 (Phase 5)**: Depends on T004-T005; it does not depend on User
  Story 2 verification.
- **Phase 6 (Final Evidence)**: Depends on T006-T009 and must run in task order so
  the capture contains final observed evidence.

### User Story Dependencies

- **User Story 1 (P1)**: First deliverable and suggested MVP.
- **User Story 2 (P1)**: Reuses the User Story 1 helper and independently verifies
  unchanged invalid-input propagation.
- **User Story 3 (P2)**: Reuses the User Story 1 helper and independently verifies
  immutability and existing-validator compatibility.

### Within Each Story

- The complete focused suite is written and observed red before application code.
- `labeling_service/area.py` precedes its package export and green story tests.
- Focused story evidence precedes full regression and session capture.
- Session capture follows all final tests; developer review follows capture.

### Parallel Opportunities

- After T004-T005, T007 and T008 are independent read-only test runs.
- T009 changes only `README.md` and can run in parallel with T007 or T008 after
  the public helper exists.
- Final regression, capture, and review remain sequential because later evidence
  depends on exact earlier outcomes.

---

## Parallel Example

After T004-T005 complete:

```text
Task T007: Verify unchanged invalid-input propagation in tests/test_box_area.py
Task T008: Verify input immutability and determinism in tests/test_box_area.py
Task T009: Add the public calculate_box_area example to README.md
```

---

## Implementation Strategy

### MVP First

1. Complete T001-T003 to establish the baseline and red contract.
2. Complete T004-T006 for User Story 1.
3. Stop and validate exact areas and public import independently.

### Incremental Delivery

1. Baseline plus complete test-first contract.
2. User Story 1: exact validated area calculation.
3. User Story 2: unchanged invalid-input propagation evidence.
4. User Story 3: immutability, compatibility, and public documentation.
5. Final focused tests, full regression, quickstart, traceability, capture, and
   developer review.

### Scope Controls

- Add no UI, HTTP server, database, model training, vehicle-control behavior, or
  dependency.
- Do not modify `labeling_service/validation.py`, `tests/test_validation.py`, the
  annotation envelope, or existing synthetic examples.
- Do not clip, round, coerce, normalize, relabel, catch, translate, or silently
  recover from invalid annotations.
