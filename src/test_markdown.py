import unittest

from markdown_utils import BlockType, MarkdownBlock, extract_title, markdown_to_blocks, parse_markdown_block


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line      

       
      
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestParseMarkdownBlock(unittest.TestCase):
    def test_parse_heading(self):
        self.assertEqual(
            parse_markdown_block("### hello"),
            MarkdownBlock(BlockType.HEADING, "hello", level=3)
        )

    def test_parse_wrong_heading_as_paragraph(self):
        self.assertEqual(
            parse_markdown_block("####### hello"),
            MarkdownBlock(BlockType.PARAGRAPH, "####### hello")
        )

    def test_parse_code(self):
        self.assertEqual(
            parse_markdown_block("```\nprint('hello')\n```"),
            MarkdownBlock(BlockType.CODE, "print('hello')")
        )

    def test_parse_wrong_code_as_paragraph(self):
        self.assertEqual(
            parse_markdown_block("```\nprint('hello')\n``"),
            MarkdownBlock(BlockType.PARAGRAPH, "``` print('hello') ``")
        )

    def test_parse_quote(self):
        self.assertEqual(
            parse_markdown_block("> hello\n> world"),
            MarkdownBlock(BlockType.QUOTE, "hello\nworld")
        )

    def test_parse_wrong_quote_as_paragraph(self):
        self.assertEqual(
            parse_markdown_block("> hello\n< world"),
            MarkdownBlock(BlockType.PARAGRAPH, "> hello < world")
        )

    def test_parse_unordered_list(self):
        self.assertEqual(
            parse_markdown_block("- hello\n- world"),
            MarkdownBlock(BlockType.ULIST, "", items=["hello", "world"])
        )

    def test_parse_wrong_unordered_list_as_paragraph(self):
        self.assertEqual(
            parse_markdown_block("- hello\n-- world"),
            MarkdownBlock(BlockType.PARAGRAPH, "- hello -- world")
        )

    def test_parse_ordered_list(self):
        self.assertEqual(
            parse_markdown_block("1. hello\n2. world"),
            MarkdownBlock(BlockType.OLIST, "", items=["hello", "world"])
        )

    def test_parse_wrong_ordered_list_as_paragraph(self):
        self.assertEqual(
            parse_markdown_block("1. hello\n3. world"),
            MarkdownBlock(BlockType.PARAGRAPH, "1. hello 3. world")
        )


class TestExtractTitle(unittest.TestCase):
    def test_correct_title(self):
        markdown = "# Hello"
        self.assertEqual(
            extract_title(markdown),
            "Hello"
        )

if __name__ == "__main__":
    unittest.main()
