from dotenv import load_dotenv

from pipeline.vector_index import load_vector_index


def main() -> None:
    # 把 .env 内容加载到当前 Python 进程
    load_dotenv()

    # 从 data/index 加载已经构建好的向量索引
    index = load_vector_index()

    # 创建检索器，只返回最相关的 3 个 Nodes
    retriever = index.as_retriever(
        similarity_top_k=3,
    )

    question = "What number should I call about benefits?"

    # 这里会把 question 转为 embedding，
    # 然后与已有的 12 个 node embeddings 比较。
    results = retriever.retrieve(question)

    for rank, result in enumerate(results, start=1):
        node = result.node

        print(f"\n--- Result {rank} ---")
        print(f"Score: {result.score}")
        print(f"Title: {node.metadata.get('title')}")
        print(f"Section: {node.metadata.get('header_path')}")
        print(f"Source: {node.metadata.get('source_url')}")
        print()
        print(node.get_content())


if __name__ == "__main__":
    main()