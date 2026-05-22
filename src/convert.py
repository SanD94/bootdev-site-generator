from markdown_utils import BlockType, MarkdownBlock, markdown_to_blocks, parse_markdown_block
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utils import text_to_textnodes

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("url doesn't exist")
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("url doesn't exist")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

def block_to_html_node(block: MarkdownBlock) -> ParentNode:
    match block.block_type:
        case BlockType.PARAGRAPH: 
            return paragraph_to_html_node(block)
        case BlockType.HEADING: 
            return heading_to_html_node(block)
        case BlockType.CODE: 
            return code_to_html_node(block)
        case BlockType.QUOTE: 
            return quote_to_html_node(block)
        case BlockType.ULIST: 
            return ulist_to_html_node(block)
        case BlockType.OLIST: 
            return olist_to_html_node(block)


def text_to_children(text: str) -> list[HTMLNode]:
    return list(map(
        lambda text_node: text_node_to_html_node(text_node),
        text_to_textnodes(text)
    ))

def paragraph_to_html_node(block: MarkdownBlock) -> ParentNode:
    return ParentNode("p", text_to_children(block.content))

def heading_to_html_node(block: MarkdownBlock) -> ParentNode:
    return ParentNode(f"h{block.level}", text_to_children(block.content))

def code_to_html_node(block: MarkdownBlock) -> ParentNode:
    code = LeafNode("code", block.content)
    return ParentNode("pre", [code])

def quote_to_html_node(block: MarkdownBlock) -> ParentNode:
    return ParentNode("blockquote", text_to_children(block.content))

def ulist_to_html_node(block: MarkdownBlock) -> ParentNode:
    if block.items is None:
        raise ValueError("unordered list items are missing")
    return ParentNode(
        "ul",
        list(map(
            lambda item: ParentNode("li", text_to_children(item)),
            block.items
        ))
    )

def olist_to_html_node(block: MarkdownBlock) -> ParentNode:
    if block.items is None:
        raise ValueError("ordered list items are missing")
    return ParentNode(
        "ol",
        list(map(
            lambda item: ParentNode("li", text_to_children(item)),
            block.items
        ))
    )

def markdown_to_html_node(markdown: str) -> ParentNode:
    return ParentNode(
        "div", 
        list(map(
            lambda block: block_to_html_node(parse_markdown_block(block)),
            markdown_to_blocks(markdown)
        ))
    )
