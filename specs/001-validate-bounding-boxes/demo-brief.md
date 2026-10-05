# Live feature brief: validate submitted bounding boxes

Status: DEMO INPUT, not a completed `/speckit.specify` output.

As a labeling reviewer, I want invalid bounding boxes rejected before they enter a
dataset, so downstream training and evaluation see one unambiguous contract.

Resolve ADAS-LBL-001, ADAS-LBL-002 and ADAS-LBL-003 through DOORS MCP in module
ADAS/Labeling at baseline DEMO-ADAS-2026.10. Then generate the feature specification,
plan and tasks using the installed templates and constitution.

The intentionally useful learning scenario is the right/bottom image boundary:
`x_max == width` is valid in a half-open pixel-edge contract. An engineer familiar
with inclusive pixel indices may incorrectly reject it. Write the acceptance test
before implementation, capture the reviewed decision and propose a product lesson
about adapter contracts rather than claiming a new department-wide policy.

Expected examples for a 1920 x 1080 frame:

| Box | Result |
|-----|--------|
| (0, 0, 1920, 1080) | Accept: complete frame |
| (1919, 1079, 1920, 1080) | Accept: one pixel at lower-right edge |
| (10, 10, 10, 20) | Reject: zero width |
| (-1, 0, 20, 20) | Reject: outside frame |
| (0, 0, 1921, 1080) | Reject: outside frame |
| (0, 0, 0.5, 1) | Reject: fractional pixel edge |
| (false, 0, 1, 1) | Reject: boolean is not a coordinate |

Do not build vehicle behavior. Keep the implementation scoped to annotation
validation and tests; choose the service stack during the live planning step.
