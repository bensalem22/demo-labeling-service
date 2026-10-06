# Data Model: Calculate Box Area

This feature creates no stored entity and changes no annotation field. It consumes
the existing annotation mapping and returns one derived integer.

## Existing validated annotation

The helper accepts the unchanged schema 1.0 annotation described by the first
feature. The existing validator remains authoritative for:

- frame identity, positive dimensions, and annotation revision;
- schema version and pixel-edge coordinate space;
- ontology and class;
- closed box shape and integer coordinate types;
- half-open ordering and frame bounds.

The helper neither reproduces these rules nor creates a second annotation model.

## Existing bounding box

| Field | Existing type | Role in calculation |
|-------|---------------|---------------------|
| `x_min` | Validated integer pixel edge | Subtracted from `x_max`. |
| `y_min` | Validated integer pixel edge | Subtracted from `y_max`. |
| `x_max` | Validated integer pixel edge | Right edge; may equal frame width. |
| `y_max` | Validated integer pixel edge | Bottom edge; may equal frame height. |

The helper reads these values only after validation succeeds.

## Derived box area

| Property | Contract |
|----------|----------|
| Type | Positive integer |
| Unit | Square pixels |
| Formula | `(x_max - x_min) * (y_max - y_min)` |
| Persistence | None |
| Annotation membership | None; it is not added to the envelope |

## Validation failure

The helper does not create an error model. If the existing validator raises
`AnnotationValidationError`, the same exception instance, code, error sequence,
and rejected result propagate to the caller.

## Relationships and lifecycle

- One helper invocation consumes one existing annotation.
- Successful validation permits one area calculation and one integer return.
- Failed validation produces no area.
- Neither path changes annotation, revision, review, dataset, or lineage state.

## Invariants

1. The existing validator runs before coordinates are read for calculation.
2. The annotation is deeply equal before and after every invocation.
3. No `area` field is added.
4. Valid area is positive and deterministic.
5. Existing validation failures are not caught, translated, or reconstructed.
