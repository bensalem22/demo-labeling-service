---
name: speckit-adas-capture
description: Prepare a sanitized session decision record; do not publish automatically.
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: Bosch demo authors
  source: extension:adas
---

# Adas Capture Skill

Read the feature spec, tasks, test results and ADR decisions.
Using only deliberately shareable information from the current session, draft
`docs/session-notes/<feature>.json` using the example schema in
`docs/session-notes/example.json`. Record:

- context and observed problem;
- chosen approach and concise engineering rationale;
- alternatives considered and why they were not selected;
- actual test commands and observed outcomes;
- evidence links to the feature, requirement, ADR or PR file;
- a candidate lesson and intended service/product/department scope.

Do NOT extract hidden reasoning, copy transcripts, inspect transcript paths,
include secrets or raw drive data, or claim a test ran when it did not.
This is an authored decision summary, not a model's private reasoning trace.
Set `approved_for_sharing` to false. Ask the developer to redact and approve it.
Only the developer may set approval to true before committing it to the PR.
Do not copy the example's scenario or test outcomes as if they were observed.
