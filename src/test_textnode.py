import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_ne_TextType(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_ne_Text(self):
        node1 = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a test node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)        

    def test_eq_link_url(self):
        node1 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        self.assertEqual(node1, node2)  

    def test_ne_link_url(self):
        node1 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://arrl.org")
        self.assertNotEqual(node1, node2)               

    def test_ne_url_None(self):
        node1 = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode("This is a test node", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_eq_No_Text(self):
        node1 = TextNode("", TextType.BOLD)
        node2 = TextNode("", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_BOLD(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_ITALIC(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_CODE(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)        

    def test_LINK(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")  
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_IMAGE(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://boot.dev/image1")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "img")  
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev/image1", "alt": "alt text"})
       






if __name__ == "__main__":
    unittest.main()

