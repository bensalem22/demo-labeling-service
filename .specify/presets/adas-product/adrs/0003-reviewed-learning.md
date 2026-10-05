# ADR-0003: PR-triggered, evidence-grounded learning

Status: Accepted for synthetic demo | Owner: Developer experience and data governance

Use a GitHub PR event to invoke a documentation agent with the PR title/body,
changed-file patches and developer-approved session decision records.
The local Copilot Stop hook only reminds the developer to prepare that record.
It does not upload chat transcripts and cannot detect all ways a PR may be opened.

The agent returns a structured proposal with source references, applicability,
limitations and promotion scope. Automation validates the output and stores it as
a short-lived workflow artifact. It has no permission to merge, approve, update
DOORS or write policy. A human promotes an accepted lesson into a governance PR.

Rejected alternatives: scraping private reasoning traces; automatically changing
constitutions; treating untrusted PR text as agent instructions; executing PR-head
scripts in a privileged documentation workflow.

An empty candidate list is valid only with an explicit evidence-based explanation.
Missing evidence, authentication failures and malformed model output fail visibly.
