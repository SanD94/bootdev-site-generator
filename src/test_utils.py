import unittest

from textnode import TextNode, TextType
from utils import (
    split_nodes_delimiter,
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_correct_begin_split(self):
        node  = TextNode("_italic text_ in a text node", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(nodes[1].text_type, TextType.PLAIN)

    def test_correct_mid_split(self):
        node  = TextNode("a text node _in the middle_ with italic", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text_type, TextType.PLAIN)

    def test_correct_end_split(self):
        node  = TextNode("a text node with italic _at the end_", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)

    def test_incorrect_split(self):
        node  = TextNode("_italic text in a text node", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_correct_extract(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        md_images = extract_markdown_images(text)
        self.assertEqual(len(md_images), 1)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_correct_extract(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        md_links = extract_markdown_links(text)
        self.assertEqual(len(md_links), 1)


class TestSplitNodeImages(unittest.TestCase):
    def test_split_image_beginning(self):
        node = TextNode("![image](url) after", TextType.PLAIN)

        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" after", TextType.PLAIN),
            ],
        )

    def test_split_image_middle(self):
        node = TextNode(
            "This is text with an ![image](url) inside",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_image([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" inside", TextType.PLAIN),
            ],
        )

    def test_split_image_end(self):
        node = TextNode("before ![image](url)", TextType.PLAIN)

        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("before ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "url"),
            ],
        )


class TestSplitNodeLinks(unittest.TestCase):
    def test_split_link_beginning(self):
        node = TextNode("[text](url) after", TextType.PLAIN)

        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("text", TextType.LINK, "url"),
                TextNode(" after", TextType.PLAIN),
            ],
        )

    def test_split_link_middle(self):
        node = TextNode(
            "This is text with an [text](url) inside",
            TextType.PLAIN,
        )

        new_nodes = split_nodes_link([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("text", TextType.LINK, "url"),
                TextNode(" inside", TextType.PLAIN),
            ],
        )

    def test_split_link_end(self):
        node = TextNode("before [text](url)", TextType.PLAIN)

        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("before ", TextType.PLAIN),
                TextNode("text", TextType.LINK, "url"),
            ],
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )




if __name__ == "__main__":
    unittest.main()

