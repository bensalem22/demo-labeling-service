# ADAS data labeling service - demo consumer

This is the developer-side repository starter. It consumes reviewed governance and
owns its [service constitution](.specify/service-constitution.md), feature specs,
code and tests. No production labeling application is preimplemented.

1. Run the governance bootstrap against this folder with a verified release.
2. Open this folder directly in VS Code.
3. Start the synthetic `doors` MCP server and verify its three read-only tools.
4. Follow [the feature brief](specs/001-validate-bounding-boxes/demo-brief.md):
   `/speckit-adas-requirements`, `/speckit-specify`, `/speckit-clarify`,
   `/speckit-plan`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement`.
5. Run actual feature tests. Verify the implementation post-hook invoked
   `/speckit-adas-capture` to prepare a
   [session note](docs/session-notes/example.json). Review, redact and explicitly
   approve only the note you intend to share. Leave the example unapproved.
6. Commit the bootstrap baseline to the default branch **before** opening the
   feature PR so the PR workflow can use trusted base-branch scripts.
7. Open a non-draft PR. Download the proposed lessons artifact and review it.
   Promote only approved, evidence-supported lessons to the governance repository.

The Stop hook is a reminder in the VS Code Local harness, not a PR webhook.
The PR workflow works regardless of whether the developer opens the PR through
VS Code, a browser or GitHub CLI.

## Annotation validation

The importable `labeling_service.validate_annotation` function validates one
synthetic annotation against the schema 1.0 half-open pixel-edge contract. Invalid
input raises `AnnotationValidationError` with stable code-and-field details.
Validation does not mutate input, persist data, review labels, release datasets,
train models or control vehicles.

Run the standard-library test suite from PowerShell:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Inspect synthetic inputs under [examples/](examples/). See the
[public validation contract](specs/001-validate-bounding-boxes/contracts/validation.md)
and [validation quickstart](specs/001-validate-bounding-boxes/quickstart.md) for
the exact interface and acceptance scenarios.

## Local specialization

Edit the service constitution source, not the generated effective constitution.
After review, rerun the same bootstrap with `--recompose`; department/product
content remains pinned. Do not use `/speckit-constitution` to replace the generated
policy; request a change to the correct source layer instead.

Feature specs and local ADRs are ordinary service-owned files. Propose exceptions
explicitly; local files cannot silently weaken department or product obligations.

## Replacing the synthetic DOORS facade

Review the installed MCP configuration and extension command with requirements
engineering. Replace the local stdio server with an organization-approved HTTP MCP
endpoint exposing equivalent read-only tool contracts, using VS Code's supported
authentication flow. Keep credentials out of Git and bundles.
Real DOORS APIs, identities, permissions and baseline semantics must be implemented
and tested by the facade owner; this demo does not assert native DOORS connectivity.

## Learning evidence limits

[The PR collector](tools/lessons.py) keeps the complete agent prompt within 90,000
bytes. It preserves the PR description and approved session notes, then prioritizes
whole implementation/test patches, requirements/contracts/ADRs, supporting context,
and finally generated assets. Paths break ties; smaller later patches can fit when
an earlier patch cannot. This is deterministic preprocessing, not an extra AI call.

Omitted patches receive metadata-only summaries in the proposal's `source.excluded`,
including reason, priority, patch size and available change counts. They are not
reviewed code evidence. Unapproved session notes remain excluded, and an oversized
required context still fails visibly rather than truncating approved notes.

This collector hotfix must reach the PR's base branch because the workflow checks
out the base SHA. Trigger a new PR event after merging it; rerunning the old failed
run still uses its old base commit. The original governance release/lock stays
unchanged, so its bootstrap will report this reviewed local hotfix as managed-file
drift until it is incorporated in a new release and migration.
