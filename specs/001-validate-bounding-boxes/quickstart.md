# Quickstart: Validate Bounding Boxes

This guide describes the validation commands to run after implementation. It does
not indicate that application code or tests already exist.

## Prerequisites

- Open PowerShell at the repository root.
- Use the repository virtual environment's Python executable.
- Do not install additional packages; the feature uses the standard library.

## Verify the public import

```powershell
.\.venv\Scripts\python.exe -c "from labeling_service import validate_annotation, AnnotationValidationError; print('import ok')"
```

Expected after implementation: the command exits successfully and prints
`import ok`.

## Run all feature tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected after implementation: every planned validation, contract, example, and
non-mutation test passes. Record the actual count and outcome only when the tests
have been run.

## Required acceptance scenarios

The tests must demonstrate:

1. A complete-frame `(0, 0, 1920, 1080)` box is accepted.
2. A lower-right `(1919, 1079, 1920, 1080)` one-pixel box is accepted.
3. Boolean and fractional coordinates are rejected without conversion.
4. Zero-area, reversed, negative, and over-boundary geometry is rejected.
5. Missing or invalid frame provenance is rejected.
6. Unknown schema, coordinate space, ontology, class, and fields are rejected.
7. Multiple independent errors are returned in the documented stable order.
8. Invalid box shape suppresses dependent coordinate and geometry errors.
9. The input mapping and nested box are unchanged on accepted and rejected paths.
10. Every valid JSON example passes and every invalid JSON example raises the
    named validation exception.

See [validation.md](./contracts/validation.md) for the public interface and
[data-model.md](./data-model.md) for the exact annotation shape.

## Scope confirmation

Successful validation means only that the submitted synthetic annotation conforms
to the input contract. It does not create revision history, establish human review,
authorize dataset release, train a model, or provide vehicle-control behavior.
