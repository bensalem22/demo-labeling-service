from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from .validation import validate_annotation


def calculate_box_area(annotation: Mapping[str, object]) -> int:
    validate_annotation(annotation)
    box = cast(Mapping[str, int], annotation["box"])
    return (box["x_max"] - box["x_min"]) * (box["y_max"] - box["y_min"])
