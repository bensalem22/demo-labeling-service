# Data labeling service constitution

Version: 1.0.0 | Owner: Labeling service team
Inherits: Engineering department 1.0.0 and ADAS product 1.0.0

## S1. Service scope

Create, validate, version and review 2D bounding-box annotations on frames from
test drives. This repository is not an object detector, a model-training pipeline
or a vehicle controller. The first feature is contract validation for submitted
annotations; UI and persistence can be planned as separate features.

## S2. Contract specialization

Follow product ADR-0001 exactly. Enforce positive integer frame dimensions,
nonempty frame identity, schema 1.0, pixel-edge coordinates, ontology
DEMO-ROAD-USERS-1 and its allowed classes. Reject invalid input with named errors;
never silently clip, round or convert. A valid right/bottom endpoint equals W/H.

## S3. Acceptance and delivery

Bind the first feature to module ADAS/Labeling, baseline DEMO-ADAS-2026.10,
requirements ADAS-LBL-001@3, ADAS-LBL-002@2 and ADAS-LBL-003@1.
Verify these through DOORS MCP before generating the implementation plan.
Test exact boundaries, one-pixel boxes, zero area, swapped edges, out-of-range
coordinates, fractional values, booleans and unknown ontology/class.

## S4. Ownership and learning

Changes to the shared annotation contract require product council review.
Service-only implementation decisions can use local ADRs. A PR includes a
developer-reviewed session summary or an explicit statement that none is shared.
Generated lesson proposals do not become policy until approved by their scope owner.

Keep this source file editable by the service team. Bootstrap composes the effective
constitution from all three layers; do not hand-edit the generated effective file.
