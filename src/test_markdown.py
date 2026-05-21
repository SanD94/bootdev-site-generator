import unittest

from markdown_utils import BlockType, block_to_block_type, markdown_to_blocks


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

class TestBlockToBlockType(unittest.TestCase):
    def test_correct_heading(self):
        block = "###### hello"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_wrong_heading(self):
        block = "####### hello"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_correct_code(self):
        block = """```\nconsole.log("Hello World!");\n```"""
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_wrong_code(self):
        block = """```\nconsole.log("Hello World!");\n``"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_correct_quote(self):
        block = """> Nope\n> Hey"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_wrong_quote(self):
        block = """> Nope\n< Hey"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_correct_ulist(self):
        block = """- nope\n- hey"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ULIST
        )

    def test_wrong_ulist(self):
        block = """- nope\n-- hey"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )


    def test_correct_olist(self):
        block = """1. nope\n2. hey"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.OLIST
        )

    def test_wrong_olist(self):
        block = """1. nope\n3. hey"""

        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

if __name__ == "__main__":
    unittest.main()

