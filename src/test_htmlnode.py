import unittest

from htmlnode import HTMLNode, LeafNode



class TestHTMLNode(unittest.TestCase):
    def test_exists_props_to_html(self):
        tag_html = HTMLNode("a", "go here", None, { "link" : "boot.dev" })
        prop_str = " link=\"boot.dev\""
        self.assertEqual(tag_html.props_to_html(), prop_str)

    def test_none_props_to_html(self):
        tag_html = HTMLNode("a", "go here", None, None)
        prop_str = ""
        self.assertEqual(tag_html.props_to_html(), prop_str)

    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            HTMLNode().to_html()

class TestLeafNode(unittest.TestCase):
    def test_to_html_val_err(self):
        with self.assertRaises(ValueError):
            LeafNode(None, None).to_html()

    def test_to_html_only_val(self):
        leafNode = LeafNode(None, "hello world!")
        htmlStr = "hello world!"
        self.assertEqual(leafNode.to_html(), htmlStr)

    def test_to_html_tag(self):
        leafNode = LeafNode("a", "hello world!", {"href" : "boot.dev"})
        htmlStr = "<a href=\"boot.dev\">hello world!</a>"
        self.assertEqual(leafNode.to_html(), htmlStr)

if __name__ == "__main__":
    unittest.main()

