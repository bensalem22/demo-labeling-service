## Department governance (required)

### Intended use and assurance

This feature validates synthetic 2D bounding-box annotation submissions before they
can be considered for later review or dataset workflows. It is labeling-toolchain
software only: it does not detect objects, train models, control a vehicle, release
datasets, or establish that an annotation is correct.

The Labeling service team owns implementation assurance and acceptance evidence.
Requirements Engineering owns interpretation of the pinned DOORS requirements, and
the ADAS data architecture council owns the shared annotation contract in
ADR-0001. Safety specialists, not this specification, determine whether any
ISO 26262, ISO 21448, Automotive SPICE, or tool-qualification obligations apply.
No ASIL, certification, compliance, or production-safety claim is made.

### Requirement provenance and acceptance mapping

The following snapshot was retrieved read-only from the synthetic DOORS MCP
module and is limited to the selected requirements. Every row preserves the
pinned revision; a newer current revision must be handled through impact analysis
rather than silently replacing this baseline.

| Requirement | Revision | Module / baseline | Status | Source URI | Retrieved UTC | Acceptance criterion | Planned test / evidence |
|-------------|----------|-------------------|--------|------------|---------------|----------------------|-------------------------|
| ADAS-LBL-001 | 3 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-001 | 2026-10-05T19:19:24.703463+00:00 | For positive integer W,H require `0 <= x_min < x_max <= W` and `0 <= y_min < y_max <= H`. | Accept valid interior boxes; reject zero-area, reversed, negative, and over-boundary boxes with named errors. |
| ADAS-LBL-001 | 3 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-001 | 2026-10-05T19:19:24.703463+00:00 | Accept complete-frame and one-pixel boxes including right and bottom endpoints W,H. | Accept `(0,0,1920,1080)` and `(1919,1079,1920,1080)` on a 1920 by 1080 frame. |
| ADAS-LBL-001 | 3 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-001 | 2026-10-05T19:19:24.703463+00:00 | Reject booleans, fractional values, zero area, reversed edges and out-of-range coordinates. | Exercise each invalid category independently and verify the corresponding named error with unchanged input. |
| ADAS-LBL-001 | 3 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-001 | 2026-10-05T19:19:24.703463+00:00 | Require schema_version 1.0 and coordinate_space pixel_edges; never silently clip or convert. | Reject missing or unsupported contract fields and verify no input value is clipped, rounded, or converted. |
| ADAS-LBL-002 | 2 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-002 | 2026-10-05T19:19:25.148591+00:00 | Require a nonempty frame ID, positive integer frame dimensions and annotation revision. | In scope: reject each missing or invalid input-provenance field with a named error. |
| ADAS-LBL-002 | 2 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-002 | 2026-10-05T19:19:25.148591+00:00 | A correction creates a new annotation revision linked to the same source frame. | Deferred: revision-history behavior requires a separate feature and is not satisfied by this validator. |
| ADAS-LBL-002 | 2 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-002 | 2026-10-05T19:19:25.148591+00:00 | Only reviewed annotations are eligible for an approved dataset. | Deferred: review-state and dataset-release gating require separate features and are not satisfied by this validator. |
| ADAS-LBL-003 | 1 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-003 | 2026-10-05T19:19:25.610614+00:00 | Require ontology DEMO-ROAD-USERS-1. | Accept the required ontology and reject missing or different ontology identifiers with a named error. |
| ADAS-LBL-003 | 1 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-003 | 2026-10-05T19:19:25.610614+00:00 | Accept car, truck, pedestrian and cyclist; reject unknown classes and ontologies explicitly. | Accept every allowed class and reject an unknown class independently with a named error. |

All selected requirements were approved at retrieval. The feature-intent search
returned no matches, so no inferred search result was substituted; the exact IDs
were retrieved after baseline membership was verified. No selected requirement is
unavailable, draft, or conflicting. ADAS-LBL-002 remains only partially covered
because its revision-history and dataset-release criteria are explicitly deferred.

### Data governance and failure behavior

- Only synthetic annotation metadata and coordinates are used for this demo.
- The validator requires no production imagery, location data, credentials, or
  other personal or confidential vehicle data.
- This feature performs validation only and does not retain, transmit, or persist
  submissions or validation results.
- Authentication, authorization, and retention controls belong to any future
  transport or persistence boundary and are outside this feature.
- Invalid submissions fail explicitly with named errors. They are never repaired,
  clipped, rounded, normalized, relabeled, or accepted through fallback behavior.
- Boundary evidence includes exact frame edges, a lower-right one-pixel box,
  invalid coordinate types, zero or reversed area, and out-of-range coordinates.

### Policy and approval state

The feature applies the already accepted synthetic-demo contract in ADR-0001 and
does not change that contract, so no new product-contract exception is requested.
Any later expansion into revision history, review state, dataset release, UI,
transport, persistence, model behavior, or vehicle behavior requires separate
scope approval before implementation. No agent-generated proposal or session
record is considered approved.

# Feature Specification: Validate Bounding Boxes

**Feature Branch**: `001-validate-bounding-boxes`

**Created**: 2026-10-05

**Status**: Draft

**Input**: Validate submitted bounding-box annotations on synthetic test-drive
frames against the pinned half-open pixel-edge, provenance, and ontology contracts.

## Clarifications

### Session 2026-10-05

- Q: When one annotation has multiple independent defects, which errors should validation return? → A: All detected errors in a fixed documented order.
- Q: What information should each validation error contain in the result contract? → A: A required error code and field name only.
- Q: Should annotations containing fields outside the documented top-level and box shape be accepted or rejected? → A: Reject unknown fields with a named error.
- Q: When invalid field types or frame dimensions make geometry comparisons impossible, should dependent geometry errors be omitted? → A: Report independent errors but omit geometry errors whose prerequisite values are invalid.
- Q: How should a missing or non-object box value be reported? → A: Return one `INVALID_BOX` error for `box` and omit dependent coordinate and geometry errors.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Accept contract-valid annotations (Priority: P1)

As a labeling reviewer, I want valid annotation submissions accepted at the exact
image boundaries so that complete-frame and edge-touching objects are not rejected
by an off-by-one interpretation.

**Why this priority**: Correct acceptance of the canonical contract is the minimum
useful validator behavior and prevents valid labels from being lost.

**Independent Test**: Submit complete-frame, lower-right one-pixel, and valid
interior boxes with complete provenance and an allowed ontology/class; each is
accepted without changing any submitted value.

**Acceptance Scenarios**:

1. **Given** a 1920 by 1080 frame and a complete valid envelope, **When** the box
   `(0, 0, 1920, 1080)` is validated, **Then** it is accepted as a complete-frame
   half-open box.
2. **Given** a 1920 by 1080 frame and a complete valid envelope, **When** the box
   `(1919, 1079, 1920, 1080)` is validated, **Then** it is accepted as the
   lower-right one-pixel box.
3. **Given** the required ontology, **When** otherwise valid annotations use each
   of `car`, `truck`, `pedestrian`, and `cyclist`, **Then** each annotation is
   accepted.

---

### User Story 2 - Reject invalid geometry without repair (Priority: P1)

As a labeling reviewer, I want invalid coordinates rejected with explicit named
errors so that malformed geometry cannot enter downstream work or be silently
changed into a different annotation.

**Why this priority**: Silent clipping, rounding, conversion, or ambiguous error
reporting would undermine the shared annotation contract.

**Independent Test**: Submit one example for every invalid geometry and coordinate
type category; each is rejected with the specified error name, and the submitted
values remain unchanged.

**Acceptance Scenarios**:

1. **Given** a valid envelope, **When** a coordinate is a boolean, **Then** the
   submission is rejected with `INVALID_COORDINATE_TYPE`.
2. **Given** a valid envelope, **When** a coordinate is fractional, **Then** the
   submission is rejected with `INVALID_COORDINATE_TYPE` without rounding.
3. **Given** a valid envelope, **When** equal minimum and maximum edges create zero
   width or height, **Then** the submission is rejected with `ZERO_AREA_BOX`.
4. **Given** a valid envelope, **When** a minimum edge exceeds its maximum edge,
   **Then** the submission is rejected with `REVERSED_BOX_EDGES`.
5. **Given** a valid envelope, **When** any edge is negative or exceeds the frame
   width or height, **Then** the submission is rejected with
   `BOX_OUT_OF_BOUNDS` without clipping.

---

### User Story 3 - Reject missing or incompatible contract metadata (Priority: P1)

As a labeling reviewer, I want submissions with missing provenance or incompatible
schema, coordinate-space, ontology, or class metadata rejected explicitly so that
an accepted annotation has one unambiguous interpretation and source frame.

**Why this priority**: Geometry alone is insufficient without the frame identity,
dimensions, annotation revision, and versioned semantic contract needed to
interpret it.

**Independent Test**: Remove or invalidate each required envelope field one at a
time and submit unsupported ontology and class values; each case is rejected with
its corresponding named error.

**Acceptance Scenarios**:

1. **Given** a submission with an empty or missing frame identity, **When** it is
   validated, **Then** it is rejected with `MISSING_FRAME_ID`.
2. **Given** non-positive, boolean, fractional, or missing frame dimensions,
   **When** the submission is validated, **Then** it is rejected with
   `INVALID_FRAME_DIMENSIONS`.
3. **Given** an empty or missing annotation revision, **When** the submission is
   validated, **Then** it is rejected with `INVALID_ANNOTATION_REVISION`.
4. **Given** a schema version other than `1.0` or coordinate space other than
   `pixel_edges`, **When** the submission is validated, **Then** it is rejected
   with `UNSUPPORTED_SCHEMA_VERSION` or `UNSUPPORTED_COORDINATE_SPACE`.
5. **Given** a missing or different ontology identifier, **When** the submission
   is validated, **Then** it is rejected with `UNSUPPORTED_ONTOLOGY`.
6. **Given** ontology `DEMO-ROAD-USERS-1` and an unlisted class, **When** the
   submission is validated, **Then** it is rejected with `UNKNOWN_CLASS`.

### Edge Cases

- The full-image box `(0, 0, W, H)` is valid for positive integer dimensions.
- The lower-right one-pixel box `(W-1, H-1, W, H)` is valid.
- A one-pixel box on any image edge is valid when both dimensions are positive.
- An endpoint equal to `W` or `H` is valid; an endpoint greater than either bound
  is invalid.
- Zero width and zero height are invalid even when all coordinates are in range.
- Reversed horizontal and vertical edges are distinguished from zero-area edges.
- Negative coordinates are out of bounds.
- Booleans are invalid as coordinates and frame dimensions even in environments
  where they can otherwise be treated as integers.
- Fractional and numeric-text coordinates are not rounded or converted.
- An empty string does not satisfy frame identity or annotation revision.
- If a submission has multiple defects, it is rejected and every reported error
  must use a name defined by this specification. All detected errors are returned
  once each in the fixed order defined by the named validation errors table; no
  reported error may imply that input was repaired.
- Missing or invalid coordinates or frame dimensions do not produce speculative
  zero-area, reversed-edge, or out-of-bounds errors because the required geometry
  comparison cannot be performed.
- A missing or non-object `box` produces one `INVALID_BOX` error and no dependent
  coordinate or geometry errors.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The validator MUST accept a bounding box only when all four
  coordinates are integers other than booleans and satisfy
  `0 <= x_min < x_max <= frame_width` and
  `0 <= y_min < y_max <= frame_height`.
- **FR-002**: The validator MUST accept endpoints equal to the frame width or
  height, including complete-frame and lower-right one-pixel boxes.
- **FR-003**: The validator MUST reject boolean, fractional, and otherwise
  non-integer coordinate values with `INVALID_COORDINATE_TYPE`.
- **FR-004**: The validator MUST reject equal opposing edges with
  `ZERO_AREA_BOX`, reversed opposing edges with `REVERSED_BOX_EDGES`, and
  negative or over-boundary edges with `BOX_OUT_OF_BOUNDS`.
- **FR-005**: The validator MUST require positive integer frame width and height,
  excluding booleans, and reject missing or invalid dimensions with
  `INVALID_FRAME_DIMENSIONS`.
- **FR-006**: The validator MUST require a nonempty frame identity and reject its
  absence with `MISSING_FRAME_ID`.
- **FR-007**: The validator MUST require a positive integer annotation revision,
  excluding booleans, and reject missing, boolean, fractional, zero, or negative values with
  `INVALID_ANNOTATION_REVISION`.
- **FR-008**: The validator MUST require schema version `1.0` and coordinate space
  `pixel_edges`, rejecting missing or different values with
  `UNSUPPORTED_SCHEMA_VERSION` and `UNSUPPORTED_COORDINATE_SPACE`, respectively.
- **FR-009**: The validator MUST require ontology `DEMO-ROAD-USERS-1`, rejecting a
  missing or different ontology with `UNSUPPORTED_ONTOLOGY`.
- **FR-010**: The validator MUST accept only `car`, `truck`, `pedestrian`, and
  `cyclist` class labels and reject any other or missing class with
  `UNKNOWN_CLASS`.
- **FR-011**: The validation result MUST unambiguously identify whether the
  submission is accepted. An accepted result MUST contain no errors. A rejected
  result MUST contain every detected applicable code-and-field error pair exactly
  once, ordered first by the named validation errors table and then by annotation
  field order. Error entries MUST contain only `code` and `field`.
- **FR-012**: Validation MUST NOT clip, round, coerce, normalize, relabel, or
  otherwise alter submitted values.
- **FR-013**: Validation MUST NOT create annotation revisions, change revision
  history, determine review state, approve annotations, or control dataset
  eligibility.
- **FR-014**: The feature MUST remain limited to validation and MUST NOT add a UI,
  HTTP server, database, model training, object detection, or vehicle-control
  behavior.
- **FR-015**: The validator MUST accept only the fields and nesting defined by the
  annotation input contract.
- **FR-016**: The validator MUST reject every unknown top-level or bounding-box
  field with `UNKNOWN_FIELD`, identify its submitted field path, and leave the
  submission unchanged.
- **FR-017**: The validator MUST evaluate zero-area, reversed-edge, and
  out-of-bounds conditions only when all four coordinates and both frame
  dimensions are valid integers and the dimensions are positive. It MUST still
  report every independently detectable shape, field, and type error.
- **FR-018**: The validator MUST reject a missing or non-object `box` with one
  `INVALID_BOX` error for field `box` and MUST omit dependent coordinate and
  geometry errors.

**Annotation input contract**

An annotation submission has exactly this logical shape:

| Field | Type | Constraint |
|-------|------|------------|
| `frame_id` | String | Required and contains at least one character; no trimming or conversion is performed. |
| `frame_width` | Integer | Required, greater than zero, and not a Boolean. |
| `frame_height` | Integer | Required, greater than zero, and not a Boolean. |
| `annotation_revision` | Integer | Required, greater than zero, and not a Boolean. |
| `schema_version` | String literal | Required and exactly `1.0`. |
| `coordinate_space` | String literal | Required and exactly `pixel_edges`. |
| `ontology` | String literal | Required and exactly `DEMO-ROAD-USERS-1`. |
| `class_label` | String literal | Required and exactly one of `car`, `truck`, `pedestrian`, or `cyclist`. |
| `box` | Object | Required and contains exactly `x_min`, `y_min`, `x_max`, and `y_max`; a missing or non-object value is `INVALID_BOX`. |
| `box.x_min` | Integer | Required, not a Boolean, and satisfies the geometry constraints. |
| `box.y_min` | Integer | Required, not a Boolean, and satisfies the geometry constraints. |
| `box.x_max` | Integer | Required, not a Boolean, and satisfies the geometry constraints. |
| `box.y_max` | Integer | Required, not a Boolean, and satisfies the geometry constraints. |

No other top-level or `box` fields are allowed. Validation reads this submission
without changing it and produces a separate validation result.

**Validation result contract**

Every result has exactly this logical shape:

| Field | Type | Constraint |
|-------|------|------------|
| `accepted` | Boolean | `true` only when `errors` is empty; otherwise `false`. |
| `errors` | Ordered list of error entries | Empty for accepted input; contains all detected errors for rejected input. |
| `errors[].code` | Named error | One of the codes in the named validation errors table. |
| `errors[].field` | Field path | One of the field paths allowed for that code in the named validation errors table. |

Error entries contain no free-form message. Duplicate `code` and `field` pairs are
not allowed. Codes are ordered by the table below. Repeated codes for different
fields are ordered by annotation field order:
`frame_id`, `frame_width`, `frame_height`, `annotation_revision`,
`schema_version`, `coordinate_space`, `ontology`, `class_label`, `box`,
`box.x_min`, `box.y_min`, `box.x_max`, `box.y_max`. Unknown field paths are
ordered lexically within `UNKNOWN_FIELD`.

Shape, required-field, literal, and type errors are detected independently.
Geometry errors (`ZERO_AREA_BOX`, `REVERSED_BOX_EDGES`, and
`BOX_OUT_OF_BOUNDS`) are evaluated only when all coordinate and frame-dimension
prerequisites are valid. Omitted dependent geometry errors are not considered
detected errors. `INVALID_BOX` also suppresses dependent coordinate,
unknown-box-field, and geometry errors.

### Named validation errors

| Error name | Allowed field path | Meaning |
|------------|--------------------|---------|
| `MISSING_FRAME_ID` | `frame_id` | Frame identity is absent or empty. |
| `INVALID_FRAME_DIMENSIONS` | `frame_width`, `frame_height` | The indicated dimension is absent, non-integer, boolean, or not positive. |
| `INVALID_ANNOTATION_REVISION` | `annotation_revision` | Annotation revision is absent, non-integer, boolean, or not positive. |
| `UNSUPPORTED_SCHEMA_VERSION` | `schema_version` | Schema version is absent or is not `1.0`. |
| `UNSUPPORTED_COORDINATE_SPACE` | `coordinate_space` | Coordinate space is absent or is not `pixel_edges`. |
| `INVALID_BOX` | `box` | The bounding-box value is absent or is not an object. |
| `INVALID_COORDINATE_TYPE` | `box.x_min`, `box.y_min`, `box.x_max`, `box.y_max` | The indicated coordinate is boolean, fractional, or otherwise not an integer. |
| `ZERO_AREA_BOX` | `box` | Opposing horizontal or vertical edges are equal. |
| `REVERSED_BOX_EDGES` | `box` | A minimum edge is greater than its corresponding maximum edge. |
| `BOX_OUT_OF_BOUNDS` | `box.x_min`, `box.y_min`, `box.x_max`, `box.y_max` | The indicated coordinate is negative or exceeds its frame boundary. |
| `UNSUPPORTED_ONTOLOGY` | `ontology` | Ontology is absent or is not `DEMO-ROAD-USERS-1`. |
| `UNKNOWN_CLASS` | `class_label` | Class is absent or is not one of the four allowed road-user classes. |
| `UNKNOWN_FIELD` | Submitted unknown top-level path or `box.<name>` | The indicated field is outside the closed annotation input contract. |

### Key Entities

- **Annotation submission**: The immutable input considered by validation,
  containing exactly the required frame provenance, contract metadata,
  ontology/class metadata, and one bounding box defined by the annotation input
  contract.
- **Frame provenance**: A nonempty frame identity, positive integer width and
  height, and positive integer annotation revision that establish the source
  context available to this validator.
- **Bounding box**: Four integer pixel-edge coordinates in the displayed,
  orientation-normalized frame using top-left origin and half-open extent.
- **Validation result**: An `accepted` Boolean and ordered `errors` list whose
  entries contain only a named `code` and annotation `field`; it does not
  represent review approval or dataset release.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the complete-frame, lower-right one-pixel, and valid
  interior synthetic examples are accepted without value changes.
- **SC-002**: 100% of the specified boolean, fractional, zero-area, reversed,
  negative, and over-boundary synthetic examples are rejected with their
  applicable named errors.
- **SC-003**: 100% of tests that independently omit or invalidate frame identity,
  frame dimensions, annotation revision, schema version, coordinate space,
  ontology, or class are rejected with the corresponding named error.
- **SC-004**: All four allowed road-user classes are accepted under
  `DEMO-ROAD-USERS-1`, and every tested unknown class or ontology is rejected.
- **SC-005**: Validation evidence demonstrates zero clipping, rounding, coercion,
  conversion, or mutation across all accepted and rejected examples.
- **SC-006**: Traceability review maps every in-scope acceptance criterion from
  ADAS-LBL-001@3, ADAS-LBL-002@2, and ADAS-LBL-003@1 to at least one acceptance
  scenario and planned test, while clearly marking the two deferred
  ADAS-LBL-002 criteria as unsatisfied by this feature.

## Assumptions

- Inputs are synthetic annotation metadata; no image content is required for
  coordinate validation.
- The source frame has already been orientation-normalized before validation.
- Each submission in this first feature contains one bounding box; collection
  validation can be added later without changing the per-box contract.
- Validation consumes submitted values as-is. Parsing external transport formats
  and deciding whether textual values represent numbers are responsibilities of a
  future boundary feature.
- Validation does not establish human review, semantic label correctness,
  suitability for training/evaluation, or safety-related fitness.

## Deferred follow-ups

- **Revision history**: Define correction behavior that creates a new immutable
  annotation revision linked to the same frame, satisfying the second acceptance
  criterion of ADAS-LBL-002@2.
- **Review and dataset release**: Define review-state transitions and enforce that
  only reviewed annotations can enter approved datasets, satisfying the third
  acceptance criterion of ADAS-LBL-002@2.
- These follow-ups require separate specifications and scope approval. Until then,
  ADAS-LBL-002@2 is only partially covered by input-provenance validation.

## ADAS product contract and lineage

### Impacted boundaries and contracts

- **Labeling boundary**: Directly impacted. It validates annotation submissions
  against schema `1.0`, coordinate space `pixel_edges`, and ontology
  `DEMO-ROAD-USERS-1`.
- **Frame catalog boundary**: Referenced only through immutable frame identity and
  positive dimensions supplied with the submission; no catalog integration is
  added.
- **Dataset curation, training, and evaluation boundaries**: Not implemented or
  modified. They benefit later from explicit rejection of malformed labels, but
  validator acceptance does not authorize dataset inclusion or constitute
  training/evaluation evidence.

### Annotation contract

- Coordinates describe pixel edges in the displayed, orientation-normalized
  source frame with top-left origin, x increasing right, and y increasing down.
- Boxes are half-open: `[x_min, x_max) x [y_min, y_max)`.
- Frame dimensions and coordinates are integers excluding booleans.
- The envelope carries nonempty frame identity, positive integer annotation
  revision, schema `1.0`, coordinate space `pixel_edges`, and ontology
  `DEMO-ROAD-USERS-1`.
- Allowed classes are `car`, `truck`, `pedestrian`, and `cyclist`.
- This feature produces a validation outcome, not a proposed, reviewed, rejected,
  or released annotation revision.

### Lineage, downstream impact, and learning

Validation preserves submitted provenance by leaving input unchanged and reporting
contract violations explicitly. No dataset manifest, split assignment, training
run, model, or evaluation evidence is created, so split integrity and downstream
release state remain unchanged. Future workflows must retain immutable annotation
revision links and independently enforce human review before dataset inclusion.

The applicable approved architecture decision is product ADR-0001, Canonical 2D
bounding-box contract. The useful demo lesson about right/bottom endpoints remains
a proposal for later reviewed capture: adapter contracts should state half-open
edge semantics explicitly. It is not accepted policy merely because it appears in
this draft specification.
