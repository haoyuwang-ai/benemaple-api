from pipeline.node_builder import build_nodes


def main() -> None:
    nodes = build_nodes()

    print(f"Created {len(nodes)} nodes.\n")

    for index, node in enumerate(nodes, start=1):
        print(f"--- Node {index} ---")
        print("Metadata:", node.metadata)
        print(node.get_content())
        print()


if __name__ == "__main__":
    main()