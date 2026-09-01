import unittest
from TextNodeUtil import markdown_to_blocks, block_to_block_type, BlockType
#from TextNodeUtil import is_heading_block
#from TextNodeUtil import is_code_block
#from TextNodeUtil import is_quote_block
#from TextNodeUtil import is_unordered_list_block
#from TextNodeUtil import is_ordered_list_block

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

    def test_markdown_heading_1(self):
        md = "# Markdown heading test 1 (one leading hash, one space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING_BLOCK )

    def test_markdown_heading_2(self):
        md = "## Markdown heading test 2 (two leading hash, one space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING_BLOCK )

    def test_markdown_heading_3(self):
        md = "### Markdown heading test 3 (three leading hash, one space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING_BLOCK )

    def test_markdown_heading_4(self):
        md = "#### Markdown heading test 4 (four leading hash, one space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING_BLOCK )

    def test_markdown_heading_5(self):
        md = "##### Markdown heading test 5 (five leading hash, one space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING_BLOCK )

    def test_markdown_heading_6(self):
        md = "###### Markdown heading test 6 (six leading hash, one space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.HEADING_BLOCK )

    def test_markdown_heading_7(self):
        md = "junk ## Markdown heading test 7 (two non-leading hash, one space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_heading_8(self):
        md = "##Markdown heading test 8 (two leading hash, missing space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH ) 

    def test_markdown_heading_9(self):
        md = "Markdown heading test 9 (no hash, no space)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH ) 

    def test_markdown_code_1(self):
        md = "```\n Markdown code test 1 (3 leading backticks, one newline, 3 ending backticks)```"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.CODE_BLOCK )

    def test_markdown_code_2(self):
        md = "```\n Markdown code test 2 (3 leading backticks, 2 newlines, \n3 ending backticks)```"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.CODE_BLOCK )

    def test_markdown_code_3(self):
        md = "```\n Markdown code test 3 (3 leading backticks, 1 newline, 2 embedded backticks ``, 1 newline, \n3 ending backticks)```"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.CODE_BLOCK )

    def test_markdown_code_4(self):
        md = "``\n Markdown code test 4 (only 2 leading backticks, 1 newline, 1 newline, \n3 ending backticks)```"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH ) 

    def test_markdown_code_5(self):
        md = "``` Markdown code test 5 (3 leading backticks, missing newline, 1 newline, \n3 ending backticks)```"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_code_6(self):
        md = "```\n Markdown code test 6 (3 leading backticks, 1 newline, 1 newline, \n2 ending backticks)``"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_code_7(self):
        md = "junk```\n Markdown code test 7 (3 non-leading backticks, 1 newline, 1 newline, \n3 ending backticks)```"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_code_8(self):
        md = "```\n Markdown code test 8 (3 leading backticks, 1 newline, 1 newline, \n3 non-ending backticks)```junk"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_quote_1(self):
        md = "> Markdown quote test 1 (leading angle bracket and space, one newline \n> leading angle & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.QUOTE_BLOCK )

    def test_markdown_quote_2(self):
        md = "< Markdown quote test 2 (leading back angle bracket and space, one newline \n> leading angle & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )  

    def test_markdown_quote_3(self):
        md = ">Markdown quote test 3 (leading angle bracket, no space, one newline \n> leading angle & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.QUOTE_BLOCK )

    def test_markdown_quote_4(self):
        md = "> Markdown quote test 4 (leading angle bracket and space, inline > one newline \n> leading angle & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.QUOTE_BLOCK )

    def test_markdown_unordered_list_1(self):
        md = "- Markdown unordered list test 1 (leading dash and space, one newline \n- leading dash & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST_BLOCK ) 

    def test_markdown_unordered_list_2(self):
        md = "_ Markdown unordered list test 2 (leading non-dash and space, one newline \n- leading dash & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_unordered_list_3(self):
        md = "-Markdown unordered list test 3 (leading dash and no space, one newline \n- leading dash & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_unordered_list_4(self):
        md = "- Markdown unordered list test 4 (leading dash and space, one newline \n-leading dash & no space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_unordered_list_5(self):
        md = "- \n- leading dash & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST_BLOCK )

    def test_markdown_ordered_list_1(self):
        md = "1. Markdown ordered list test 1 (leading one dot and space, one newline \n2. leading two dot & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST_BLOCK )

    def test_markdown_ordered_list_2(self):
        md = "1 Markdown ordered list test 2 (leading one, no dot, and space, one newline \n2. leading two dot & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_ordered_list_3(self):
        md = "1.Markdown ordered list test 3 (leading one dot and no space, one newline \n2. leading two dot & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )

    def test_markdown_ordered_list_4(self):
        md = "1. Markdown ordered list test 4 (leading one dot and space, one newline \n3. leading three dot & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )   

    def test_markdown_ordered_list_5(self):
        md = "2. Markdown ordered list test 5 (leading two dot and space, one newline \n2. leading two dot & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )  

    def test_markdown_ordered_list_6(self):
        md = "A1. Markdown ordered list test 6 (leading A one dot and space, one newline \n2. leading two dot & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )             

    def test_markdown_ordered_list_7(self):
        md = "1. Markdown ordered list test 7 (leading one dot and space, one newline \nB. leading B dot & space, final line)"
        blocktype = block_to_block_type(md)
        self.assertEqual(blocktype, BlockType.NORMAL_PARAGRAPH )                                                                                                                              