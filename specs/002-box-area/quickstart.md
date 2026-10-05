# Quickstart: Calculate Box Area

This guide defines the commands and public example to validate after
implementation. It does not claim the helper or tests already exist.

## Prerequisites

- Open PowerShell at the repository root.
- Use `.\.venv\Scripts\python.exe`.
- Install no additional packages.

## Focused helper tests

```powershell
.\.venv\Scripts\python.exe -m unittest -v tests.test_box_area
```

Expected after implementation: focused area, propagation, immutability, and public
import tests pass.

## Full regression

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected after implementation: all pre-existing validator tests and all new area
tests pass. Record actual counts and outcomes only after running the commands.

## Short public API example

```python
import json
from pathlib import Path

from labeling_service import calculate_box_area

annotation = json.loads(
    Path("examples/valid/full_image.json").read_text(encoding="utf-8")
)
print(calculate_box_area(annotation))
```

Expected output:

```text
2073600
```

See [box-area.md](./contracts/box-area.md) for the public contract and
[data-model.md](./data-model.md) for the unchanged annotation relationship.
