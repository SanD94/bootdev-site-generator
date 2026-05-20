import re
from textnode import TextNode, TextType

def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimiter: str,
        text_type: TextType) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            nodes.append(node)
            continue
        split_texts = node.text.split(delimiter)

        if len(split_texts) % 2 == 0:
            raise ValueError("delimiter should be in pairs")

        new_nodes: list[TextNode] = []
        for i, text in enumerate(split_texts):
            if i % 2 == 1:
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, TextType.PLAIN))
        nodes.extend(filter(lambda node: node.text != "", new_nodes))

    return nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    md_img_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(md_img_regex, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    md_link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(md_link_regex, text)
    

