# ADR-0002: Read-only DOORS access and explicit baseline changes

Status: Accepted for synthetic demo | Owner: Requirements engineering

DOORS remains the system of record. Agents query an authorized MCP facade using
exact module, requirement IDs and baseline. The facade returns immutable
revision metadata and source links. No write tool is exposed in this demo.

Specs retain a reviewed snapshot of the relevant requirement intent and provenance,
not a bulk copy of DOORS. At planning/review time, compare pinned requirements
with current status. Newer revisions create an impact-analysis task; they do not
rewrite a feature's baseline. Missing or draft inputs stop affected work.

An HTTP MCP facade for real DOORS must enforce access controls, pagination,
rate/size limits, audit logging and data classification on the server. Prompt
instructions alone are not an authorization boundary. Transport credentials
are supplied through approved identity flows, never embedded in a bundle.
