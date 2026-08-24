import unittest
from TextNodeUtil import markdown_to_blocks

class TestMDNode(unittest.TestCase):
    def test_markdown_to_blocks1(self):
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

    def test_markdown_to_blocks2(self):
        md = """
This is a paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- To **boldly** go
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- To **boldly** go\n- with items",
            ],
        )        

    def test_markdown_to_blocks3(self):
        md = """
This is a paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- [IBM logo](https://ibm.com)
- [HP logo](https://hp.com)
- [Dell logo](https://dell.com)
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- [IBM logo](https://ibm.com)\n- [HP logo](https://hp.com)\n- [Dell logo](https://dell.com)",
            ],
        )

    def test_markdown_to_blocks4(self):
        md = """
This paragraph had 3 blank following lines



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This paragraph had 3 blank following lines",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks5(self):
        md = """
   This paragraph had 3 leading spaces

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This paragraph had 3 leading spaces",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )     