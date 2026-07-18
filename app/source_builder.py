from llama_index.core.schema import NodeWithScore

from app.schemas import SourceResponse


def build_sources(
    source_nodes: list[NodeWithScore],
) -> list[SourceResponse]:
    sources: list[SourceResponse] = []
    seen_sources: set[tuple[str, str]] = set()

    for source_node in source_nodes:
        node = source_node.node

        title = node.metadata.get("title", "")
        url = node.metadata.get("source_url", "")
        header_path = node.metadata.get("header_path", "")

        content = node.get_content().strip()
        first_line = content.splitlines()[0] if content else ""
        first_line = first_line.lstrip("# ").strip()

        if header_path and header_path != "/":
            section = header_path
        else:
            section = first_line or "Unknown section"

        source_key = (url, section)

        if source_key in seen_sources:
            continue

        seen_sources.add(source_key)

        sources.append(
            SourceResponse(
                score=source_node.score,
                title=title,
                section=section,
                url=url,
            )
        )

    return sources