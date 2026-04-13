import unittest

from htmlnode import HTMLNode



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


if __name__ == "__main__":
    unittest.main()

