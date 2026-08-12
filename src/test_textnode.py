import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)

    def test_ne_TextType(self):
        node1 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node1, node2)

    def test_ne_Text(self):
        node1 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is a test node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node1, node2)        

    def test_eq_link_url(self):
        node1 = TextNode("This is a text node", TextType.LINK_TEXT, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK_TEXT, "https://boot.dev")
        self.assertEqual(node1, node2)  

    def test_ne_link_url(self):
        node1 = TextNode("This is a text node", TextType.LINK_TEXT, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK_TEXT, "https://arrl.org")
        self.assertNotEqual(node1, node2)               

    def test_ne_url_None(self):
        node1 = TextNode("This is a text node", TextType.LINK_TEXT, "https://boot.dev")
        node2 = TextNode("This is a test node", TextType.LINK_TEXT)
        self.assertNotEqual(node1, node2)

    def test_eq_No_Text(self):
        node1 = TextNode("", TextType.BOLD_TEXT)
        node2 = TextNode("", TextType.BOLD_TEXT)
        self.assertEqual(node1, node2)    

if __name__ == "__main__":
    unittest.main()

