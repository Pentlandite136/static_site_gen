import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode


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

    def test_to_html_with_0_children(self):
        parent_node = ParentNode("p", []) 
        self.assertEqual(parent_node.to_html(), "<p></p>")        
    
    def test_to_html_with_1_child(self):
        child_node = LeafNode("i", "italic child") 
        parent_node = ParentNode("p", [child_node]) 
        self.assertEqual(parent_node.to_html(), "<p><i>italic child</i></p>")              

    def test_to_html_with_2_children(self):
        child_node = LeafNode("span", "child") 
        parent_node = ParentNode("div", [child_node]) 
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_4_children(self):
        child1_node = LeafNode("b", "bold child")
        child2_node = LeafNode(None, "normal child") 
        child3_node = LeafNode("i", "italic child")
        child4_node = LeafNode(None, "normal child")
        parent_node = ParentNode("p", [child1_node, child2_node, child3_node, child4_node]) 
        self.assertEqual(parent_node.to_html(), "<p><b>bold child</b>normal child<i>italic child</i>normal child</p>")                

    def test_to_html_with_1_grandchildren(self):
        grandchild1_node = LeafNode("b", "grandchild1")
        child_node = ParentNode("span", [grandchild1_node])
        parent_node = ParentNode("div", [child_node]) 
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild1</b></span></div>")

    def test_to_html_with_2_grandchildren(self):
        grandchild1_node = LeafNode("b", "grandchild1")
        grandchild2_node = LeafNode("i", "grandchild2")
        child_node = ParentNode("span", [grandchild1_node, grandchild2_node])
        parent_node = ParentNode("div", [child_node]) 
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild1</b><i>grandchild2</i></span></div>")  

    def test_to_html_with_2_children_4_grandchildren(self):
        gchild1_node = LeafNode("b", "gchild1")
        gchild2_node = LeafNode("i", "gchild2")
        gchild3_node = LeafNode("p", "gchild3")
        gchild4_node = LeafNode("span", "gchild4")
        child1_node = ParentNode("span", [gchild1_node, gchild2_node, gchild3_node])
        child2_node = ParentNode("h1", [gchild4_node])
        parent_node = ParentNode("div", [child1_node, child2_node]) 
        self.assertEqual(parent_node.to_html(), "<div><span><b>gchild1</b><i>gchild2</i><p>gchild3</p></span><h1><span>gchild4</span></h1></div>")      



if __name__ == "__main__":
    unittest.main()

