# Data Model: Validate Bounding Boxes

This feature has no storage model. The entities below define the in-memory,
read-only validation boundary and immutable validation evidence.

## Annotation

An annotation is a closed mapping with these required fields:

| Field | Logical type | Validation |
|-------|--------------|------------|
| `frame_id` | String | At least one character; input is not trimmed or converted. |
| `frame_width` | Integer | Positive and not Boolean. |
| `frame_height` | Integer | Positive and not Boolean. |
| `annotation_revision` | Integer | Positive and not Boolean. |
| `schema_version` | String | Exactly `1.0`. |
| `coordinate_space` | String | Exactly `pixel_edges`. |
| `ontology` | String | Exactly `DEMO-ROAD-USERS-1`. |
| `class_label` | String | `car`, `truck`, `pedestrian`, or `cyclist`. |
| `box` | Mapping | Exactly the four coordinate fields described below. |

Unknown annotation fields are invalid and produce `UNKNOWN_FIELD` with their
submitted top-level path.

## Bounding Box

| Field | Logical type | Validation |
|-------|--------------|------------|
| `x_min` | Integer | Not Boolean; `0 <= x_min < x_max`. |
| `y_min` | Integer | Not Boolean; `0 <= y_min < y_max`. |
| `x_max` | Integer | Not Boolean; `x_max <= frame_width`. |
| `y_max` | Integer | Not Boolean; `y_max <= frame_height`. |

Coordinates use integer pixel edges in the displayed, orientation-normalized
source frame. The box is half-open:
`[x_min, x_max) x [y_min, y_max)`. An endpoint equal to frame width or height is
valid. Unknown box fields are invalid and use the `box.<name>` path.

A missing or non-mapping `box` produces only `INVALID_BOX` for dependent box
validation. Missing or invalid individual coordinate values produce
`INVALID_COORDINATE_TYPE` for their field. Geometry checks run only after all
coordinates and frame dimensions pass type and positivity prerequisites.

## Validation Error

An immutable error value contains exactly:

| Field | Type | Rule |
|-------|------|------|
| `code` | String | One stable named code from the specification. |
| `field` | String | The exact annotation path associated with the defect. |

The same `(code, field)` pair appears at most once. Code order follows the named
validation error table in `spec.md`; known field order follows the annotation
shape, and unknown paths are lexical within `UNKNOWN_FIELD`.

## Validation Result

An immutable result contains:

| Field | Type | Rule |
|-------|------|------|
| `accepted` | Boolean | True exactly when `errors` is empty. |
| `errors` | Immutable ordered sequence of Validation Error | Empty for accepted input; complete detected set for rejected input. |

## Annotation Validation Error

The public named exception represents a rejected validation result:

| Attribute | Type | Rule |
|-----------|------|------|
| `code` | String | Stable value `ANNOTATION_VALIDATION_FAILED`. |
| `result` | Validation Result | Always has `accepted=False` and a nonempty error sequence. |
| `errors` | Immutable ordered sequence | Exposes the same sequence as `result.errors`. |

Human-readable exception text is diagnostic only and is not part of the stable
machine contract.

## Relationships and lifecycle

- One Annotation contains one Bounding Box.
- One validation invocation produces one successful Validation Result or raises
  one Annotation Validation Error carrying one rejected Validation Result.
- A Validation Result contains zero or more Validation Errors.
- Validation creates no annotation revision and changes no annotation state.
- Proposed, reviewed, rejected, released, and dataset-eligible states are outside
  this feature.

## Invariants

1. Caller input is deeply equal before and after validation.
2. Accepted results contain zero errors.
3. Rejected results contain at least one error.
4. Every error contains only code and field.
5. Error ordering is deterministic.
6. The exception's errors and rejected result errors are identical.
