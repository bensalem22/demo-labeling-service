"""Synthetic, read-only DOORS facade. No connection to real IBM DOORS."""

from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Synthetic ADAS DOORS")
MODULE = "ADAS/Labeling"
BASELINE = "DEMO-ADAS-2026.10"
REQUIREMENTS = {
    "ADAS-LBL-001": {
        "revision": 3,
        "status": "approved",
        "text": "Validate integer half-open pixel-edge boxes in the orientation-normalized frame.",
        "acceptance_criteria": [
            "For positive integer W,H require 0 <= x_min < x_max <= W and 0 <= y_min < y_max <= H.",
            "Accept complete-frame and one-pixel boxes including right and bottom endpoints W,H.",
            "Reject booleans, fractional values, zero area, reversed edges and out-of-range coordinates.",
            "Require schema_version 1.0 and coordinate_space pixel_edges; never silently clip or convert.",
        ],
    },
    "ADAS-LBL-002": {
        "revision": 2,
        "status": "approved",
        "text": "Preserve immutable frame and annotation provenance.",
        "acceptance_criteria": [
            "Require a nonempty frame ID, positive integer frame dimensions and annotation revision.",
            "A correction creates a new annotation revision linked to the same source frame.",
            "Only reviewed annotations are eligible for an approved dataset.",
        ],
    },
    "ADAS-LBL-003": {
        "revision": 1,
        "status": "approved",
        "text": "Validate the versioned road-user ontology before accepting an annotation.",
        "acceptance_criteria": [
            "Require ontology DEMO-ROAD-USERS-1.",
            "Accept car, truck, pedestrian and cyclist; reject unknown classes and ontologies explicitly.",
        ],
    },
    "ADAS-LBL-004": {
        "revision": 1,
        "status": "draft",
        "text": "Future support for partially occluded objects; not approved for implementation.",
        "acceptance_criteria": ["BLOCKED: quality thresholds require requirement-owner approval."],
    },
}


def validate_scope(module: str, baseline: str) -> None:
    if module != MODULE or baseline not in (BASELINE, "CURRENT"):
        raise ValueError(f"Unknown module/baseline: {module!r}, {baseline!r}. No fallback.")


def requirement(requirement_id: str, module: str, baseline: str) -> dict:
    validate_scope(module, baseline)
    if requirement_id not in REQUIREMENTS:
        raise ValueError(f"Requirement {requirement_id!r} not found.")
    return {
        "id": requirement_id,
        **REQUIREMENTS[requirement_id],
        "module": MODULE,
        "baseline": BASELINE if baseline != "CURRENT" else "CURRENT",
        "source_uri": f"https://doors.example.invalid/requirements/{requirement_id}",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "synthetic": True,
    }


@mcp.tool()
def get_baseline(module: str, baseline: str) -> dict:
    """Return the exact synthetic baseline and its approved requirement IDs."""
    validate_scope(module, baseline)
    return {
        "module": MODULE,
        "baseline": baseline,
        "synthetic": True,
        "requirements": [
            {"id": key, "revision": value["revision"], "status": value["status"]}
            for key, value in REQUIREMENTS.items()
        ],
    }


@mcp.tool()
def search_requirements(query: str, module: str, baseline: str) -> list[dict]:
    """Search within an explicitly selected module/baseline; empty results are explicit."""
    validate_scope(module, baseline)
    if not query.strip():
        raise ValueError("Provide a nonempty search query.")
    return [
        requirement(key, module, baseline)
        for key, value in REQUIREMENTS.items()
        if query.casefold() in (key + " " + value["text"]).casefold()
    ]


@mcp.tool()
def get_requirement(requirement_id: str, module: str, baseline: str) -> dict:
    """Return exact text, acceptance criteria and provenance, including draft status."""
    return requirement(requirement_id, module, baseline)


if __name__ == "__main__":
    mcp.run(transport="stdio")
