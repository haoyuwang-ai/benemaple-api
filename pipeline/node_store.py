import json
from collections.abc import Iterable, Iterator
from pathlib import Path

from llama_index.core.schema import BaseNode
from llama_index.core.storage.docstore.utils import doc_to_json, json_to_doc


def save_nodes_jsonl(nodes: Iterable[BaseNode], path: Path) -> int:
    """将 LlamaIndex nodes 写为可恢复的 JSONL 文件。"""

    path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with path.open("w", encoding="utf-8", newline="\n") as file:
        for node in nodes:
            payload = doc_to_json(node)
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")
            count += 1

    return count


def load_nodes_jsonl(path: Path) -> Iterator[BaseNode]:
    """从 JSONL 文件逐个恢复 LlamaIndex nodes。"""

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                payload = json.loads(line)
                yield json_to_doc(payload)
            except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid node JSONL at {path}:{line_number}"
                ) from exc
