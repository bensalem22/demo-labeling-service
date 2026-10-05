# ADR-0001: Canonical 2D bounding-box contract

Status: Accepted for synthetic demo | Owner: ADAS data architecture council
Decision date: 2026-10-05 | Requirement: ADAS-LBL-001 revision 3

## Context

Labeling UIs and downstream training libraries can disagree about normalized versus
pixel coordinates, inclusive endpoints, image rotation and integer rounding.
Numerically valid boxes can therefore describe different image regions.

## Decision

The interchange contract uses integer pixel-edge coordinates in the displayed,
orientation-normalized source frame. Origin is top-left; x increases right and y
increases down. Boxes are half-open `[x_min, x_max) x [y_min, y_max)`.

For width W and height H: `0 <= x_min < x_max <= W` and
`0 <= y_min < y_max <= H`. W and H are positive integers. Booleans are not integers
for this contract. Reject non-integers, zero-area, reversed and out-of-bounds boxes.
An edge at W or H is valid; the inclusive maximum pixel index W-1 is not the
canonical endpoint. A one-pixel box `[0, 1) x [0, 1)` has area 1.

Require frame ID, dimensions, `coordinate_space=pixel_edges`,
`schema_version=1.0` and ontology version on the annotation envelope. Ontology
DEMO-ROAD-USERS-1 contains car, truck, pedestrian and cyclist.
The same annotation revision cannot refer to a different frame.

## Alternatives

- Normalized floats: convenient for training, but rounding must be explicit.
- Inclusive pixel indices: familiar but introduces off-by-one adapter errors.
- Accept every convention: flexible but ambiguous at service boundaries.

## Consequences

UI/model adapters perform named, tested transformations and retain source
provenance. They do not silently clip invalid boxes. Contract changes require a
new schema version and migration evidence. This contract alone does not establish
label correctness or suitability for safety-related use.
