## Department governance (required)

### Intended use and assurance

This feature provides a convenience calculation for the area of one validated
synthetic 2D bounding-box annotation. It supports labeling-service consumers that
need the area represented by the existing half-open pixel-edge contract. It does
not change annotation validity, label meaning, review state, dataset eligibility,
training behavior, evaluation evidence, or vehicle behavior.

The Labeling service team owns implementation assurance and acceptance evidence.
Requirements Engineering owns interpretation of the pinned DOORS requirements,
the ADAS data architecture council owns ADR-0001, and the synthetic demo service
owner approved the service-local area requirement. Safety specialists determine
any applicable ISO 26262, ISO 21448, Automotive SPICE, or tool-qualification
obligations. This specification makes no ASIL, certification, compliance, or
production-safety claim.

### Local requirement approval

| Field | Value |
|-------|-------|
| Requirement | `LOCAL-LBL-DEMO-001` |
| Revision | `1` |
| Status | Approved |
| Scope | Labeling service only |
| Approver | Synthetic demo service owner |
| Approval provenance | Direct approval in the `/speckit-specify` feature request received 2026-10-05T14:07:43.492-07:00 |
| Requirement text | Calculate the square-pixel area of a validated annotation box using the half-open pixel-edge contract. |
| Acceptance criteria | Validate with the existing annotation validator; propagate existing named validation errors unchanged; calculate `(x_max - x_min) * (y_max - y_min)` without an inclusive-endpoint adjustment; do not modify the input or shared annotation envelope. |

`LOCAL-LBL-DEMO-001@1` is an explicitly approved local requirement under
department constitution D1. It is not a DOORS requirement, policy exception,
shared annotation-schema change, or product-contract change. This approval applies
only to the convenience helper described in this specification.

### Authoritative DOORS provenance and acceptance mapping

The following selected requirements were retrieved read-only from the synthetic
DOORS MCP module. The feature-intent search returned no matches, so no inferred
search result was substituted. Exact IDs were retrieved after baseline membership
was verified.

| Requirement | Revision | Module / baseline | Status | Source URI | Retrieved UTC | Acceptance criterion | Feature evidence |
|-------------|----------|-------------------|--------|------------|---------------|----------------------|------------------|
| ADAS-LBL-001 | 3 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-001 | 2026-10-05T21:08:09.588350+00:00 | For positive integer W,H require `0 <= x_min < x_max <= W` and `0 <= y_min < y_max <= H`. | Area is calculated only after the existing validator accepts these inequalities. |
| ADAS-LBL-001 | 3 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-001 | 2026-10-05T21:08:09.588350+00:00 | Accept complete-frame and one-pixel boxes including right and bottom endpoints W,H. | Exact area examples cover the complete frame and lower-right one-pixel box. |
| ADAS-LBL-001 | 3 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-001 | 2026-10-05T21:08:09.588350+00:00 | Reject booleans, fractional values, zero area, reversed edges and out-of-range coordinates. | Invalid annotations fail through the existing validator before area calculation. |
| ADAS-LBL-001 | 3 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-001 | 2026-10-05T21:08:09.588350+00:00 | Require schema_version 1.0 and coordinate_space pixel_edges; never silently clip or convert. | The helper accepts no alternate schema or coordinate space and performs no conversion. |
| ADAS-LBL-002 | 2 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-002 | 2026-10-05T21:08:10.184843+00:00 | Require a nonempty frame ID, positive integer frame dimensions and annotation revision. | The existing validator checks provenance before the helper reads box coordinates. |
| ADAS-LBL-002 | 2 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-002 | 2026-10-05T21:08:10.184843+00:00 | A correction creates a new annotation revision linked to the same source frame. | Not implemented or changed; the helper is a pure calculation and creates no revision. |
| ADAS-LBL-002 | 2 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-002 | 2026-10-05T21:08:10.184843+00:00 | Only reviewed annotations are eligible for an approved dataset. | Not implemented or changed; the helper does not establish review or dataset eligibility. |
| ADAS-LBL-003 | 1 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-003 | 2026-10-05T21:08:10.816056+00:00 | Require ontology DEMO-ROAD-USERS-1. | The existing validator rejects another or missing ontology before calculation. |
| ADAS-LBL-003 | 1 | ADAS/Labeling / DEMO-ADAS-2026.10 | Approved | https://doors.example.invalid/requirements/ADAS-LBL-003 | 2026-10-05T21:08:10.816056+00:00 | Accept car, truck, pedestrian and cyclist; reject unknown classes and ontologies explicitly. | Existing allowed and rejected class/ontology behavior remains unchanged and is regression tested. |
| LOCAL-LBL-DEMO-001 | 1 | Labeling service local | Approved | Local provenance above; no DOORS URI | 2026-10-05T14:07:43.492-07:00 | Return validated half-open box area without changing input or error behavior. | Exact area, error propagation, input immutability, and regression scenarios. |

All selected DOORS requirements were approved at retrieval. No unavailable, draft,
or conflicting selected requirement blocks this specification. ADAS-LBL-002
revision-history and dataset-release behavior remain outside this helper and are
not claimed as satisfied by it.

### Data governance and failure behavior

- Only synthetic annotation metadata and coordinates are used.
- The helper reads no imagery and performs no storage, transport, logging, or
  persistence.
- Invalid input fails through the existing named validation exception, preserving
  its code, ordered code-and-field errors, and rejected result unchanged.
- The helper does not clip, round, coerce, normalize, relabel, or mutate input.
- No area field is added to the annotation or shared schema.

### Policy and approval state

The helper applies ADR-0001 without changing it. No policy exception, product
council approval, or annotation-schema migration is requested. Any future change
to coordinate semantics, schema fields, validation behavior, or shared adapters
requires separate review at the appropriate scope.

# Feature Specification: Calculate Box Area

**Feature Branch**: `002-box-area`

**Created**: 2026-10-05

**Status**: Draft

**Input**: Add a service-local convenience function that returns the square-pixel
area of an annotation accepted by the existing validator.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Calculate validated box area (Priority: P1)

As a labeling-service consumer, I want the square-pixel area of a valid annotation
box so that I can use one contract-consistent calculation instead of recreating
pixel-edge arithmetic.

**Why this priority**: The helper has value only if it returns the correct area for
the existing canonical coordinate contract.

**Independent Test**: Submit each specified valid annotation and compare the
returned integer with its exact expected area while confirming the annotation is
unchanged.

**Acceptance Scenarios**:

1. **Given** a valid 1920 by 1080 complete-frame box `(0, 0, 1920, 1080)`,
   **When** area is requested, **Then** the result is `2073600`.
2. **Given** a valid lower-right one-pixel box
   `(1919, 1079, 1920, 1080)`, **When** area is requested, **Then** the result is
   `1`.
3. **Given** a valid box `(10, 20, 30, 50)`, **When** area is requested,
   **Then** the result is `600`.

---

### User Story 2 - Preserve validation failures (Priority: P1)

As a labeling-service consumer, I want invalid annotations to fail exactly as they
already do so that using the area helper cannot bypass or reinterpret validation.

**Why this priority**: Calculating from invalid geometry or translating established
errors would weaken the governed annotation boundary.

**Independent Test**: Pass representative invalid annotations through both the
validator and area helper and verify that the helper exposes the same named
exception code, ordered code-and-field errors, and rejected result.

**Acceptance Scenarios**:

1. **Given** an annotation with invalid geometry, **When** area is requested,
   **Then** the existing named validation failure is propagated unchanged and no
   area is returned.
2. **Given** an annotation with missing provenance, **When** area is requested,
   **Then** the existing named validation failure is propagated unchanged.
3. **Given** an annotation with an unknown ontology or class, **When** area is
   requested, **Then** the existing named validation failure is propagated
   unchanged.

---

### User Story 3 - Preserve annotation and validator compatibility (Priority: P2)

As the labeling service owner, I want the helper to leave the annotation contract
and existing validation behavior unchanged so that current consumers and evidence
remain valid.

**Why this priority**: The approved local helper is not approval to alter the
shared schema or existing validator.

**Independent Test**: Run the full pre-existing validation regression suite plus
new immutability checks and verify that no annotation receives an area field or
other mutation.

**Acceptance Scenarios**:

1. **Given** any valid annotation, **When** area is calculated, **Then** the input
   remains deeply equal to its original value and contains no added area field.
2. **Given** the existing validation regression suite, **When** the helper is
   introduced, **Then** every pre-existing test continues to pass unchanged.

### Edge Cases

- Complete-frame area is `W * H`, not `(W + 1) * (H + 1)`.
- A valid one-pixel half-open box has area `1`.
- A box touching the right or bottom edge uses endpoints `W` or `H` directly;
  no inclusive-endpoint `+1` adjustment is applied.
- Invalid zero-area, reversed, out-of-range, Boolean, fractional, provenance,
  schema, coordinate-space, ontology, class, and closed-shape inputs do not reach
  area calculation.
- Multiple validation errors retain their established order and fields.
- Repeated calculation with the same unchanged annotation returns the same area.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The service MUST provide `calculate_box_area(annotation)` for one
  annotation submission.
- **FR-002**: The helper MUST validate the complete annotation using the existing
  annotation validator before reading coordinates for area calculation.
- **FR-003**: For accepted input, the helper MUST return the integer square-pixel
  area `(x_max - x_min) * (y_max - y_min)`.
- **FR-004**: The helper MUST NOT add `1` to either half-open extent.
- **FR-005**: The helper MUST return `2073600` for the valid complete-frame
  1920 by 1080 example, `1` for the valid lower-right one-pixel example, and `600`
  for the valid `(10, 20, 30, 50)` example.
- **FR-006**: If validation fails, the helper MUST propagate the existing named
  validation exception and its stable exception code, ordered code-and-field
  errors, and rejected validation result unchanged.
- **FR-007**: The helper MUST NOT catch and translate validation failures into a
  new error name, fallback value, or partial area.
- **FR-008**: The helper MUST NOT clip, round, coerce, normalize, relabel, or
  otherwise alter input before or after validation.
- **FR-009**: The helper MUST NOT add an area value or any other field to the
  annotation envelope.
- **FR-010**: The helper MUST preserve every existing validator behavior and
  existing validation test.
- **FR-011**: The helper MUST NOT create annotation revisions, change review
  state, approve dataset use, persist results, add transport behavior, train a
  model, or control a vehicle.

### Key Entities

- **Validated annotation**: The existing closed schema 1.0 annotation accepted by
  the current validator; this feature adds no fields or states.
- **Bounding box**: The existing four integer pixel-edge coordinates
  `(x_min, y_min, x_max, y_max)` in the orientation-normalized frame.
- **Box area**: A positive integer number of square pixels derived from the
  validated half-open extents; it is a returned value, not annotation data.
- **Validation failure**: The existing named exception, stable exception code,
  ordered code-and-field errors, and rejected result, propagated unchanged.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the three specified valid examples return exactly
  `2073600`, `1`, and `600`, respectively.
- **SC-002**: 100% of representative invalid geometry, provenance, schema,
  coordinate-space, ontology, class, and closed-shape cases produce the same
  named exception code and ordered code-and-field errors as direct validation.
- **SC-003**: 100% of valid and invalid helper tests demonstrate that the input is
  deeply unchanged and no area field is added.
- **SC-004**: 100% of the existing validation regression suite passes without
  modification after the helper is introduced.
- **SC-005**: Traceability review links every helper behavior to
  `LOCAL-LBL-DEMO-001@1` and every reused validation/coordinate behavior to the
  applicable pinned DOORS requirement revision and ADR-0001.

## Assumptions

- The input uses the existing annotation mapping contract and contains one box.
- The current validator remains the sole authority for annotation validity.
- Because accepted coordinates are integers under ADR-0001, the returned area is
  a positive integer.
- The helper is deterministic and stateless; it stores no calculated value.
- Performance targets are not introduced because no requirement owner supplied
  one for this small in-process calculation.

## ADAS product contract and lineage

### Impacted boundaries and contracts

- **Labeling boundary**: Adds one service-local derived calculation over a
  validated annotation.
- **Shared annotation contract**: Unchanged. Schema version remains `1.0`; no area
  field or coordinate interpretation is added.
- **Frame catalog, dataset curation, training, evaluation, and release evidence**:
  No integration or state change. Helper output does not establish label review,
  dataset eligibility, or safety evidence.

### Coordinate and validation contract

- Coordinates remain integer half-open pixel edges in the displayed,
  orientation-normalized source frame.
- Width is `x_max - x_min`; height is `y_max - y_min`; area is their product.
- Right and bottom endpoints equal to frame dimensions remain valid.
- The helper performs no inclusive-endpoint adjustment and defines no alternate
  coordinate convention.
- The existing validator runs first and retains its complete public failure
  contract.

### Lineage, downstream impact, and learning

The derived area is not persisted and creates no new annotation or dataset
lineage. Downstream consumers that choose to use the returned value remain
responsible for their own approved requirements. The applicable approved
architecture decision remains ADR-0001. No lesson is promoted to service, product,
or department policy by this draft specification.
