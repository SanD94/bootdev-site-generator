import os
import re
from markdown_utils import BlockType, MarkdownBlock, extract_title, markdown_to_blocks, parse_markdown_block
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

def _replace_content(html: str, title: str, md_html_str: str) -> str:
    html = re.sub(r"\{\{ Title \}\}", title, html)
    html = re.sub(r"\{\{ Content \}\}", str(md_html_str), html)
    return html

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    md_html_str = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    content = _replace_content(template, title, md_html_str)
    dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(dest_path, "w") as f:
        f.write(content)

def _md_to_html_path(src: str, src_root: str = "content", dst_root: str = "public") -> str:
    rel = os.path.relpath(src, src_root)
    fname, _ = os.path.splitext(rel)
    return os.path.join(dst_root, fname + ".html")
        
def generate_blog(src: str = "content", dst: str = "public"):
    for dir in os.listdir(src):
        dir_path = os.path.join(src, dir)
        if os.path.isfile(dir_path):
            dst_html = _md_to_html_path(dir_path)
            generate_page(dir_path, "template.html", dst_html)
        if os.path.isdir(dir_path):
            dst_dir_path = os.path.join(dst, dir_path)
            generate_blog(dir_path, dst_dir_path)
            

    

