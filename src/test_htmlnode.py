import unittest
from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()

