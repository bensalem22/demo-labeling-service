# ADAS toolchain product constitution

Version: 1.0.0 | Inherits: Engineering department 1.0.0
Status: synthetic architecture for discussion, not a production autonomous-driving design
Owner: ADAS product architecture council

## P1. End-to-end scope and separation

The product covers test-drive ingestion, privacy processing, frame cataloging,
annotation, dataset curation, training, model registry, simulation/replay,
evaluation, release evidence and feedback. Each bounded service has its own
repository and owns its contracts. This demo implements governance, not vehicle
control or a deployable autonomous-driving system.

## P2. Stable identities and immutable lineage

Use immutable drive, sensor, frame, calibration, annotation revision, dataset and
model identifiers. Frame identity is independent of filename and processing order.
An annotation revision records its source frame, image dimensions, ontology
version, labeling protocol and reviewer. Corrections create new revisions.
Dataset manifests pin approved annotation revisions; retries cannot duplicate data.

## P3. Explicit data contracts

Never infer coordinate space, units, orientation, timestamps or calibration.
The product's 2D annotation interchange is defined in ADR-0001. Services MUST
validate it at boundaries and version breaking changes. Unknown class labels,
invalid geometry and incompatible ontology versions fail explicitly.
Adapters record transformations rather than silently clipping or rescaling labels.

## P4. Quality gates and human review

Distinguish proposed, reviewed, rejected and released labels. Only reviewed
annotations enter approved training/evaluation datasets. Prevent train/evaluation
leakage by splitting at drive/session level before sampling frames.
Report dataset coverage by conditions such as lighting and weather when authorized
metadata exists; no quality threshold is invented without a requirement owner.
Ground-truth changes trigger downstream impact analysis.

## P5. Requirements and evidence

Use the read-only DOORS MCP protocol in the installed ADAS extension. Requirement
baseline DEMO-ADAS-2026.10 is synthetic. Trace impact across annotation, datasets,
training and evaluation. A newer DOORS revision does not silently move the pinned
baseline; create a change proposal and re-run impacted acceptance tests.

## P6. Product learning loop

Service lessons about shared contracts go to the product council; broadly
applicable engineering lessons go to the department board. Reviewed lessons can
update ADRs, templates, tests and constitutions. A new signed-off release distributes
the change to every service through a reviewed bundle update.
