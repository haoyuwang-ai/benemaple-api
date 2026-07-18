from dotenv import load_dotenv

from pipeline.rag_query import create_query_engine


def main() -> None:
    load_dotenv()

    query_engine = create_query_engine()

    question = input("Question: ").strip()
    if not question:
        print("Question cannot be empty.")
        return

    response = query_engine.query(question)

    print("\nAnswer:")
    print(str(response))

    print("\nRetrieved sources:")

    seen_sources: set[tuple[str, str]] = set()

    for source in response.source_nodes:
        node = source.node

        title = node.metadata.get("title", "Unknown title")
        source_url = node.metadata.get("source_url", "")
        section = node.get_content().splitlines()[0].lstrip("# ").strip()

        source_key = (source_url, section)
        if source_key in seen_sources:
            continue

        seen_sources.add(source_key)

        print(f"- Score: {source.score}")
        print(f"  Title: {title}")
        print(f"  Section: {section}")
        print(f"  URL: {source_url}")

if __name__ == "__main__":
    main()