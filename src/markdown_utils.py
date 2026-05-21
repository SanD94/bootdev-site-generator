def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")

    blocks = list(map(lambda block: block.strip(), blocks))
    blocks = list(filter(lambda block: block != "", blocks))

    return blocks
