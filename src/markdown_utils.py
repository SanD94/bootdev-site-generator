from dataclasses import dataclass
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING   = "heading"
    CODE      = "code"
    QUOTE     = "quote"
    ULIST     = "unordered_list"
    OLIST     = "ordered_list"


@dataclass
class MarkdownBlock:
    block_type: BlockType
    content: str
    level: int | None = None
    items: list[str] | None = None


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")

    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: block != "", blocks))

    return blocks


def parse_markdown_block(md_block: str) -> MarkdownBlock:
    lines = md_block.split("\n")
    heading_match = re.match(r"^(#{1,6}) (.+)", md_block)

    if heading_match:
        return MarkdownBlock(
            BlockType.HEADING,
            heading_match.group(2),
            level=len(heading_match.group(1))
        )
    if md_block.startswith("```\n") and md_block.endswith("```"):
        return MarkdownBlock(
            BlockType.CODE,
            md_block[4:-4]
        )
    if all(line.startswith(">") for line in lines):
        return MarkdownBlock(
            BlockType.QUOTE,
            "\n".join(line[1:].strip() for line in lines)
        )
    if all(line.startswith("- ") for line in lines):
        return MarkdownBlock(
            BlockType.ULIST,
            "",
            items=[line[2:] for line in lines]
        )
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return MarkdownBlock(
            BlockType.OLIST,
            "",
            items=[line.split(". ", 1)[1] for line in lines]
        )

    return MarkdownBlock(
        BlockType.PARAGRAPH,
        " ".join(lines)
    )
