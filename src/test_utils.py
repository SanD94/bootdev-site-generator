import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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


if __name__ == "__main__":
    unittest.main()

