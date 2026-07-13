import asyncio
from pathlib import Path

from pipeline.llama_parse_client import parse_document


async def main() -> None:
    input_file = Path("data/raw/fctsht_nw_cnd-en.pdf")
    parsed = await parse_document(input_file)

    output_file = Path("data/parsed") / f"{input_file.stem}.md"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(parsed.markdown, encoding="utf-8")

    print(f"Saved: {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
