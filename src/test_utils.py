import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter

class TestSplitNodeDelimiter(unittest.TestCase):
    def test_correct_split(self):
        node  = TextNode("_italic text_ in a text node _at the end_", TextType.PLAIN)
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text_type, TextType.ITALIC)
        self.assertEqual(nodes[1].text_type, TextType.PLAIN)
        self.assertEqual(nodes[2].text_type, TextType.ITALIC)

    def test_incorrect_split(self):
        node  = TextNode("_italic text in a text node", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()

