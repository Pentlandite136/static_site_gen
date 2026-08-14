import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("a", "The value of the HTML tag", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "The value of the HTML tag", None, {"href": "https://www.google.com"})
        self.assertEqual(node1, node2)

    def test_ne_HTMLtag(self):
        node1 = HTMLNode("a", "The value of the HTML tag", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "The value of the HTML tag", None, {"href": "https://www.google.com"})
        self.assertNotEqual(node1, node2)

    def test_ne_HTMLvalue(self):
        node1 = HTMLNode("a", "The value of the HTML tag", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "The value of the XML tag", None, {"href": "https://www.google.com"})
        self.assertNotEqual(node1, node2)        

    def test_ne_link_url(self):
        node1 = HTMLNode("a", "The value of the HTML tag", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "The value of the HTML tag", None, {"href": "https://www.hp.com"})
        self.assertNotEqual(node1, node2)               

    def test_eq_No_empty_url(self):
        node1 = HTMLNode("a", "The value of the HTML tag", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "The value of the HTML tag", None, { })
        self.assertNotEqual(node1, node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>") 

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>") 

    def test_leaf_to_html_a_1(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')           

    def test_leaf_to_html_a_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Click me!</a>')           



if __name__ == "__main__":
    unittest.main()

