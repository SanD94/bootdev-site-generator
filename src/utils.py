import re
from typing import Callable, Iterator, Match
from textnode import TextNode, TextType

IMAGE_PATTERN = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINK_PATTERN  = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

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


def iter_markdown_images(text: str) -> Iterator[Match[str]]:
    return re.finditer(IMAGE_PATTERN, text)

def iter_markdown_links(text: str) -> Iterator[Match[str]]:
    return re.finditer(LINK_PATTERN, text)

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return [(match.group(1), match.group(2)) for match in iter_markdown_images(text)]

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return [(match.group(1), match.group(2)) for match in iter_markdown_links(text)]


MarkdownMatcher = Callable[[str], Iterator[Match[str]]]

def split_nodes_by_matcher(
    old_nodes: list[TextNode],
    matcher: MarkdownMatcher,
    text_type: TextType
) -> list[TextNode]:

    nodes : list[TextNode] = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            nodes.append(node)
            continue

        cursor = 0
        for match in matcher(node.text):
            start, end = match.span()
            if start > cursor:
                nodes.append(TextNode(node.text[cursor:start], TextType.PLAIN))

            text = match.group(1)
            url = match.group(2)
            nodes.append(TextNode(text, text_type, url))

            cursor = end

        if cursor < len(node.text):
            nodes.append(TextNode(node.text[cursor:], TextType.PLAIN))

    return nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_matcher(old_nodes, iter_markdown_images, TextType.IMAGE)

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_by_matcher(old_nodes, iter_markdown_links, TextType.LINK)


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text, TextType.PLAIN)
    nodes = [node]
    methods = [
        lambda nodes: split_nodes_delimiter(nodes, "**", TextType.BOLD),
        lambda nodes: split_nodes_delimiter(nodes, "_", TextType.ITALIC),
        lambda nodes: split_nodes_delimiter(nodes, "`", TextType.CODE),
        split_nodes_image,
        split_nodes_link
    ]

    for method in methods:
        nodes = method(nodes)

    return nodes
