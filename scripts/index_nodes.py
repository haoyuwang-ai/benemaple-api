from dotenv import load_dotenv

from pipeline.vector_index import build_vector_index


def main() -> None:
    build_vector_index()



if __name__ == "__main__":
    load_dotenv()
    main()
    print("Vector index saved to data/index")