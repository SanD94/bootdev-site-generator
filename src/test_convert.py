import unittest

from convert import markdown_to_html_node, text_node_to_html_node
from textnode import TextNode, TextType

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(
            html_node.props, 
            { "href": "https://boot.dev" }
        )

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://boot.dev/images")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, 
            {
                "src": "https://boot.dev/images",
                "alt": "This is an image node"
            }
        )


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_markdown_blocks_to_html(self):
        markdown = """## My _heading_

- one
- **two**

```
print("hi")
```"""

        html_node = markdown_to_html_node(markdown)

        self.assertEqual(
            html_node.to_html(),
            '<div><h2>My <i>heading</i></h2><ul><li>one</li><li><b>two</b></li></ul><pre><code>print("hi")</code></pre></div>'
        )


if __name__ == "__main__":
    unittest.main()
