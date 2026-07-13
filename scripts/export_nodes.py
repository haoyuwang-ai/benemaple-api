from pathlib import Path

from pipeline.node_builder import build_nodes
from pipeline.node_store import save_nodes_jsonl


def main() -> None:
    output_path = Path("data/nodes/nodes.jsonl")
    nodes = build_nodes()
    count = save_nodes_jsonl(nodes, output_path)

    print(f"Saved {count} nodes to {output_path}")


if __name__ == "__main__":
    main()
