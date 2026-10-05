---

description: "Test-first task list for bounding-box annotation validation"
---

# Tasks: Validate Bounding Boxes

**Input**: Design documents from `specs/001-validate-bounding-boxes/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/validation.md`, `quickstart.md`

**Tests**: Required. Every story writes focused `unittest` coverage and confirms
the new tests fail for the expected missing behavior before implementation.

**Organization**: Tasks are grouped by user story so each contract slice has an
independent acceptance checkpoint.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it changes a different file and does not
  require another incomplete task.
- **[Story]**: Maps the task to a specification user story.
- Every task names the file it creates, changes, or validates.

## Phase 1: Setup

**Purpose**: Create only the planned standard-library project skeleton.

- [X] T001 Create empty Python 3.12-compatible skeleton files `labeling_service/__init__.py`, `labeling_service/validation.py`, and `tests/test_validation.py`, plus directories `examples/valid/` and `examples/invalid/`; add no dependencies, frameworks, server, storage, model-training, or vehicle-control code

---

## Phase 2: Foundational Public Contract

**Purpose**: Establish the immutable result and named exception contract used by
all stories.

**CRITICAL**: Complete this phase before any user-story implementation.

### Tests first

- [X] T002 Write public import and contract tests in `tests/test_validation.py` for frozen `ValidationError(code, field)`, frozen `ValidationResult(accepted, errors)`, `accepted=True` exactly when errors are empty, and `AnnotationValidationError.code == "ANNOTATION_VALIDATION_FAILED"` with `exception.errors == exception.result.errors`; run only these tests with `.\.venv\Scripts\python.exe -m unittest -v tests.test_validation` and confirm they fail for the expected missing public types

### Implementation

- [X] T003 Implement only the frozen `ValidationError`, frozen `ValidationResult`, and `AnnotationValidationError` public types plus stable code and field ordering constants in `labeling_service/validation.py`; error entries contain exactly `code` and `field`, duplicate `(code, field)` pairs are not allowed in a rejected result, and exception prose is not stable contract data
- [X] T004 [P] Re-export `validate_annotation`, `AnnotationValidationError`, `ValidationError`, and `ValidationResult` from `labeling_service/__init__.py` without adding any other public surface
- [X] T005 Run the foundational tests in `tests/test_validation.py` with `.\.venv\Scripts\python.exe -m unittest -v tests.test_validation` and confirm the public types and exception contract pass before starting story behavior

**Checkpoint**: The importable immutable evidence and exception contract is ready.

---

## Phase 3: User Story 1 - Accept Contract-Valid Annotations (Priority: P1) MVP

**Goal**: Accept valid interior, complete-frame, and exact lower-right one-pixel
boxes without changing input.

**Independent Test**: Validate a complete envelope with `(0, 0, 1920, 1080)`,
`(1919, 1079, 1920, 1080)`, and an interior box; each returns
`ValidationResult(accepted=True, errors=())`, and the input remains deeply equal.

### Tests and examples first

- [X] T006 [P] Create synthetic valid annotations in `examples/valid/full_image.json` and `examples/valid/lower_right_pixel.json` with nonempty `frame_id`, positive integer dimensions and `annotation_revision`, schema `1.0`, coordinate space `pixel_edges`, ontology `DEMO-ROAD-USERS-1`, allowed class `car`, and the exact 1920 by 1080 boundary boxes
- [X] T007 [US1] Add failing tests in `tests/test_validation.py` named `test_accepts_valid_interior_box`, `test_accepts_complete_frame`, `test_accepts_lower_right_one_pixel_box`, and `test_does_not_mutate_valid_input`; run those tests and confirm failure for the expected missing acceptance behavior before implementation

### Implementation

- [X] T008 [US1] Implement the valid `validate_annotation` path in `labeling_service/validation.py` for one closed annotation mapping and one box whose coordinates are integers excluding booleans and satisfy `0 <= x_min < x_max <= frame_width` and `0 <= y_min < y_max <= frame_height`; return immutable `ValidationResult(accepted=True, errors=())` and do not trim, convert, copy back into, or otherwise mutate caller data
- [X] T009 [US1] Run the User Story 1 tests in `tests/test_validation.py` and load both `examples/valid/*.json` files through the public function; confirm exact frame edges and the lower-right one-pixel box pass independently

**Checkpoint**: Valid half-open pixel-edge annotations are accepted without mutation.

---

## Phase 4: User Story 2 - Reject Invalid Geometry Without Repair (Priority: P1)

**Goal**: Reject every invalid coordinate type and geometry category with complete,
stable errors and no clipping, rounding, coercion, or mutation.

**Independent Test**: Submit boolean, fractional, numeric-text, missing-coordinate,
zero-width, zero-height, reversed-horizontal, reversed-vertical, negative-edge,
and over-boundary cases; each raises `AnnotationValidationError` with the exact
ordered code/field pairs and leaves input unchanged.

### Tests and examples first

- [X] T010 [P] Create synthetic invalid geometry files `examples/invalid/boolean_coordinate.json`, `examples/invalid/fractional_coordinate.json`, `examples/invalid/zero_width.json`, and `examples/invalid/multiple_errors.json` without production imagery or identifying data
- [X] T011 [US2] Add failing geometry and type tests in `tests/test_validation.py` named `test_rejects_boolean_coordinate`, `test_rejects_fractional_coordinate`, `test_rejects_numeric_text_coordinate`, `test_rejects_missing_coordinate`, `test_rejects_zero_width`, `test_rejects_zero_height`, `test_rejects_reversed_horizontal_edges`, `test_rejects_reversed_vertical_edges`, `test_rejects_each_negative_edge`, `test_rejects_each_over_boundary_edge`, `test_does_not_mutate_invalid_input`, `test_returns_all_errors_in_stable_order`, `test_deduplicates_code_field_pairs`, and `test_omits_dependent_geometry_errors`; confirm they fail before implementation

### Implementation

- [X] T012 [US2] Implement coordinate and geometry rejection in `labeling_service/validation.py`: booleans, fractions, numeric text, and missing coordinates use `INVALID_COORDINATE_TYPE`; equal opposing edges use `ZERO_AREA_BOX`; minimum greater than maximum uses `REVERSED_BOX_EDGES`; negative or over-boundary coordinates use `BOX_OUT_OF_BOUNDS`; run geometry only when both positive integer dimensions and all four integer non-Boolean coordinates are valid, return all independently detectable unique code/field pairs in contract order, and never clip, round, coerce, normalize, or mutate input
- [X] T013 [US2] Run all User Story 2 tests in `tests/test_validation.py` and validate every `examples/invalid/` geometry file raises `AnnotationValidationError` with the planned stable code and field paths

**Checkpoint**: Invalid geometry is rejected explicitly and unchanged.

---

## Phase 5: User Story 3 - Reject Missing or Incompatible Metadata (Priority: P1)

**Goal**: Reject invalid provenance, schema, coordinate-space, ontology, class, and
closed-shape metadata while preserving the two deferred ADAS-LBL-002 behaviors.

**Independent Test**: Remove or invalidate each required envelope field one at a
time, exercise every allowed class, add unknown fields, and invalidate the box
shape; each case produces only the specified deterministic errors.

### Tests and examples first

- [X] T014 [P] Create synthetic invalid metadata files `examples/invalid/missing_provenance.json`, `examples/invalid/unknown_class.json`, `examples/invalid/unknown_field.json`, and `examples/invalid/unknown_ontology.json` with unchanged submitted values and no production data
- [X] T015 [US3] Add failing metadata and closed-shape tests in `tests/test_validation.py` covering missing and empty `frame_id`; missing, non-integer, Boolean, fractional, zero, and negative `frame_width`, `frame_height`, and `annotation_revision`; missing and unsupported `schema_version` and `coordinate_space`; missing and unsupported ontology; all allowed classes `car`, `truck`, `pedestrian`, and `cyclist`; missing and unknown class; unknown top-level and box fields; missing and non-mapping box; and `INVALID_BOX` suppression of dependent coordinate, unknown-box-field, and geometry errors; confirm the new tests fail before implementation

### Implementation

- [X] T016 [US3] Implement envelope and closed-shape checks in `labeling_service/validation.py`: `frame_id` is a string containing at least one character with no trimming; `frame_width`, `frame_height`, and `annotation_revision` are positive integers excluding booleans; `schema_version` is exactly `1.0`; `coordinate_space` is exactly `pixel_edges`; ontology is exactly `DEMO-ROAD-USERS-1`; class is exactly one of `car`, `truck`, `pedestrian`, or `cyclist`; unknown fields use `UNKNOWN_FIELD`; a missing or non-mapping box uses only `INVALID_BOX` for dependent box validation; do not create revision history, review state, or dataset eligibility behavior
- [X] T017 [US3] Run all User Story 3 tests in `tests/test_validation.py`, confirm each allowed class passes, confirm every provenance/ontology/shape rejection has the required code and field, and rerun User Stories 1 and 2 to detect regressions

**Checkpoint**: All three user stories are independently testable and the validator
does not claim the deferred revision-history or dataset-release requirements.

---

## Phase 6: Regression, Documentation, and Reviewed Evidence

**Purpose**: Verify the complete feature and prepare governed evidence without
self-approving it.

- [X] T018 Add example regression tests `test_all_valid_examples_pass` and `test_all_invalid_examples_raise_validation_error` in `tests/test_validation.py`, confirm the new invalid-example test fails if any invalid fixture is accepted, then make only fixture or validator corrections required by the governed contract
- [X] T019 [P] Update `README.md` with the importable validation entry point, PowerShell `unittest` command, synthetic-example locations, explicit validation-only scope, and links to `specs/001-validate-bounding-boxes/contracts/validation.md` and `specs/001-validate-bounding-boxes/quickstart.md`
- [X] T020 Run the import command and full regression command from `specs/001-validate-bounding-boxes/quickstart.md` using `.\.venv\Scripts\python.exe`, record the exact test count and outcomes for evidence, and resolve any feature-caused failures without weakening tests or changing governed contracts
- [X] T021 Execute `/speckit-adas-capture` after T020 to prepare a sanitized, synthetic, explicitly unapproved session decision record under `docs/session-notes/`; include actual commands and outcomes, the half-open right/bottom-edge decision, rejected alternatives, requirement revisions, limitations, and no raw transcript, credentials, private reasoning, invented approvals, or production data
- [X] T022 Require a developer to review and redact the generated `docs/session-notes/*.json`, verify its recorded test outcomes against T020, and explicitly approve the exact shareable record or leave it unapproved; the implementing agent MUST NOT mark its own proposal approved or promote the lesson into policy

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on T001 and blocks all story behavior.
- **User Story 1 (Phase 3)**: Depends on T002-T005.
- **User Story 2 (Phase 4)**: Depends on T002-T005; sequential execution after
  User Story 1 is recommended because both modify `validation.py` and the same
  test module.
- **User Story 3 (Phase 5)**: Depends on T002-T005; sequential execution after
  User Story 2 is recommended for the same shared-file reason.
- **Regression and evidence (Phase 6)**: T018-T020 depend on all selected stories;
  T021 depends on the completed regression; T022 is a human-review gate after T021.

### User Story Dependencies

- **US1**: No behavioral dependency after the foundational contract.
- **US2**: Uses the same public function but its rejection behavior is independently
  testable with a valid envelope.
- **US3**: Uses the same public function but its metadata behavior is independently
  testable with valid geometry.
- ADAS-LBL-002 revision-history and dataset-release behaviors remain deferred and
  have no implementation task in this feature.

### Test-First Order Within Each Story

1. Write examples and focused tests.
2. Run the new tests and confirm expected failure.
3. Implement only the story's missing behavior.
4. Run the story checkpoint.
5. Do not weaken a test to make implementation pass.

### Parallel Opportunities

- T003 and T004 modify different package files and can be authored in parallel
  after T002 establishes the contract.
- T006 can run in parallel with T007.
- T010 can run in parallel with T011.
- T014 can run in parallel with T015.
- T019 can run in parallel with T018 because it changes documentation rather than
  validator or test files.
- Story implementation tasks should not run in parallel in one worktree because
  they modify the same `labeling_service/validation.py` and
  `tests/test_validation.py` files.

---

## Parallel Examples

### User Story 1

```text
Task T006: Create valid JSON examples under examples/valid/
Task T007: Write failing valid-boundary tests in tests/test_validation.py
```

### User Story 2

```text
Task T010: Create invalid geometry examples under examples/invalid/
Task T011: Write failing geometry/type tests in tests/test_validation.py
```

### User Story 3

```text
Task T014: Create invalid metadata examples under examples/invalid/
Task T015: Write failing provenance/ontology/shape tests in tests/test_validation.py
```

---

## Implementation Strategy

### MVP First

1. Complete T001-T005.
2. Complete T006-T009 for User Story 1.
3. Stop and demonstrate complete-frame and lower-right one-pixel acceptance with
   unchanged input.

### Incremental Delivery

1. Foundation establishes stable public evidence and exception contracts.
2. US1 adds correct exact-edge acceptance.
3. US2 adds explicit geometry/type rejection without repair.
4. US3 adds provenance, ontology, class, and closed-shape enforcement.
5. Regression validates all synthetic examples and the complete public contract.
6. ADAS capture prepares evidence; a developer, not the agent, decides approval.

---

## Notes

- Every task uses Python's standard library and the repository interpreter.
- `[P]` tasks operate on different files; shared validator/test edits stay serial.
- Test names preserve the requirement-to-test mapping in `plan.md`.
- Record only actual test results after execution; this task list makes no claim
  that implementation or tests already exist or pass.
- Do not edit generated constitutions or release-managed governance files.
