import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any


def iter_catalog_entries(path: Path) -> Iterator[dict[str, Any]]:
    """逐行读取 JSONL catalog。"""

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                entry = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSONL at {path}:{line_number}"
                ) from exc

            if not isinstance(entry, dict):
                raise ValueError(
                    f"Expected a JSON object at {path}:{line_number}"
                )

            yield entry
