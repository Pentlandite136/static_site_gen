import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from TextNodeUtil import split_nodes_delimiter, extract_markdown_images, extract_markdown_links 
from TextNodeUtil import split_nodes_image, split_nodes_link, text_to_textnodes


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
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_BOLD(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_ITALIC(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_CODE(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)        

    def test_LINK(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")  
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_IMAGE(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://boot.dev/image1")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")  
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev/image1", "alt": "alt text"})

    def test_split_0_inline_text(self):
        node = [TextNode("This is not an italic text test.", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "_", TextType.ITALIC)
        self.assertEqual(len(split_node), 1)
        self.assertEqual(split_node[0].text, "This is not an italic text test.")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)

    def test_split_1_inline_text(self):
        node = [TextNode("This is an _italic text_ test.", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "_", TextType.ITALIC)
        self.assertEqual(len(split_node), 3)
        self.assertEqual(split_node[0].text, "This is an ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "italic text")
        self.assertEqual(split_node[1].text_type, TextType.ITALIC)       
        self.assertEqual(split_node[2].text, " test.")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)

    def test_split_2_inline_text(self):
        node = [TextNode("_italic text_ test.", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "_", TextType.ITALIC)
        self.assertEqual(len(split_node), 2)
        self.assertEqual(split_node[0].text, "italic text")
        self.assertEqual(split_node[0].text_type, TextType.ITALIC)       
        self.assertEqual(split_node[1].text, " test.")
        self.assertEqual(split_node[1].text_type, TextType.TEXT)

    def test_split_3_inline_text(self):
        node = [TextNode("_italic text_", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "_", TextType.ITALIC)
        self.assertEqual(len(split_node), 1)
        self.assertEqual(split_node[0].text, "italic text")
        self.assertEqual(split_node[0].text_type, TextType.ITALIC)       

    def test_split_double_inline_text1(self):
        node = [TextNode("This _is_ an _italic text_ test.", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "_", TextType.ITALIC)
        self.assertEqual(len(split_node), 5)
        self.assertEqual(split_node[0].text, "This ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "is")
        self.assertEqual(split_node[1].text_type, TextType.ITALIC)       
        self.assertEqual(split_node[2].text, " an ")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[3].text, "italic text")       
        self.assertEqual(split_node[3].text_type, TextType.ITALIC)       
        self.assertEqual(split_node[4].text, " test.")
        self.assertEqual(split_node[4].text_type, TextType.TEXT)                

    def test_split_double_inline_text2(self):
        node = [TextNode("This `J=J+1` increments variable `J` in FORTRAN.", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(len(split_node), 5)
        self.assertEqual(split_node[0].text, "This ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "J=J+1")
        self.assertEqual(split_node[1].text_type, TextType.CODE)       
        self.assertEqual(split_node[2].text, " increments variable ")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[3].text, "J")       
        self.assertEqual(split_node[3].text_type, TextType.CODE)       
        self.assertEqual(split_node[4].text, " in FORTRAN.")
        self.assertEqual(split_node[4].text_type, TextType.TEXT)

    def test_split_1_bold_inline_text(self):
        node = [TextNode("To **boldly** go where ...", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(len(split_node), 3)
        self.assertEqual(split_node[0].text, "To ")
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[1].text, "boldly")
        self.assertEqual(split_node[1].text_type, TextType.BOLD)       
        self.assertEqual(split_node[2].text, " go where ...")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)

    def test_split_mixed_inline_text(self):
        node = [TextNode("To **be** or _not _**to be** that is the question.", TextType.TEXT)]
        result1_node = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(len(result1_node), 5)
        result2_node = split_nodes_delimiter(result1_node, "_", TextType.ITALIC)
        self.assertEqual(len(result2_node), 6)
        self.assertEqual(result2_node[0].text, "To ")
        self.assertEqual(result2_node[0].text_type, TextType.TEXT)
        self.assertEqual(result2_node[1].text, "be")
        self.assertEqual(result2_node[1].text_type, TextType.BOLD)       
        self.assertEqual(result2_node[2].text, " or ")
        self.assertEqual(result2_node[2].text_type, TextType.TEXT)
        self.assertEqual(result2_node[3].text, "not ")       
        self.assertEqual(result2_node[3].text_type, TextType.ITALIC)       
        self.assertEqual(result2_node[4].text, "to be")
        self.assertEqual(result2_node[4].text_type, TextType.BOLD)
        self.assertEqual(result2_node[5].text, " that is the question.")
        self.assertEqual(result2_node[5].text_type, TextType.TEXT)

    def test_extract_markdown_images_0(self):
        matches = extract_markdown_images(
            "This is text with no image"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_1(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_2(self):
        s = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        s += " and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(s)
        image_list = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),]
        image_list.append(("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),)
        self.assertListEqual(image_list, matches)

    def test_extract_markdown_images_3(self):
        s = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        s += " and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        s += " with an intention non-image ![HP](https://hp.com)"
        matches = extract_markdown_images(s)
        image_list = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),]
        image_list.append(("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),)
        image_list.append(("HP", "https://hp.com"))
        self.assertListEqual(image_list, matches)

    def test_extract_markdown_links_0(self):
        matches = extract_markdown_links(
            "This is text with no link"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_1(self):
        matches = extract_markdown_links(
            "This is text with a [link1](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link1", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_2(self):
        s = "This is text with 2 links [link1](https://i.imgur.com/aKaOqIh.gif)"
        s += " and [link2](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(s)
        link_list = [("link1", "https://i.imgur.com/aKaOqIh.gif"),]
        link_list.append(("link2", "https://i.imgur.com/fJRm4Vk.jpeg"),)
        self.assertListEqual(link_list, matches)

    def test_extract_markdown_links_3(self):
        s = "This is text with 3 links [link1](https://i.imgur.com/aKaOqIh.gif)"
        s += " and [link2](https://i.imgur.com/fJRm4Vk.jpeg)"
        s += " with another link [link3](https://hp.com)"
        matches = extract_markdown_links(s)
        link_list = [("link1", "https://i.imgur.com/aKaOqIh.gif"),]
        link_list.append(("link2", "https://i.imgur.com/fJRm4Vk.jpeg"),)
        link_list.append(("link3", "https://hp.com"))
        self.assertListEqual(link_list, matches)


    def test_split_images_t(self):
        node = TextNode(
            "This is text with no image ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no image ", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_t(self):
        node = TextNode(
            "This is text with no link ",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no link ", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_t_i(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links_t_l(self):
        node = TextNode(
            "This is text with a link [link text](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_i_t(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_l_t(self):
        node = TextNode(
            "[link text](https://i.imgur.com/zjjcJKZ.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link text", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_i(self):
        node = TextNode(
            "![image only](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image only", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_links_l(self):
        node = TextNode(
            "[link only](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link only", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_t_i_t_i_t(self):
        node = TextNode(
            "First text ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/3elNhQu.png) and finally ![image3](https://hp.com) last text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("First text ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and finally ", TextType.TEXT),
                TextNode("image3", TextType.IMAGE, "https://hp.com"),
                TextNode(" last text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_t_l_t_l_t(self):
        node = TextNode(
            "First text [link1](https://i.imgur.com/zjjcJKZ.png) and [link2](https://i.imgur.com/3elNhQu.png) and finally [link3](https://hp.com) last text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("First text ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" and finally ", TextType.TEXT),
                TextNode("link3", TextType.LINK, "https://hp.com"),
                TextNode(" last text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_i_t_i(self):
        node = TextNode(
            "![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_l_t_l(self):
        node = TextNode(
            "[link1](https://i.imgur.com/zjjcJKZ.png) and [link2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_t_i_t(self):
        node = TextNode(
            "Leading text ![image1](https://i.imgur.com/zjjcJKZ.png) trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Leading text ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_t_l_t(self):
        node = TextNode(
            "Leading text [link1](https://i.imgur.com/zjjcJKZ.png) trailing text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Leading text ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_i_i(self):
        node = TextNode(
            "![image1](https://i.imgur.com/zjjcJKZ.png)![image2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links_l_l(self):
        node = TextNode(
            "[link1](https://i.imgur.com/zjjcJKZ.png)[link2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("link2", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_text_t_b_t_i_t_c_t_i_t_l(self):
        s = "This is **text** with an _italic_ word and a `code block` and an "
        s += "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
        s += "[link](https://boot.dev)"

        new_nodes = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_text_t_b_t_i_t_c_t_i(self):
        s = "To **boldly** go where _Italians_ have never `coded before`: "
        s += "![Mt Vesuvius](https://mtvesuvius.org/pompeii-python-coders)"

        new_nodes = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("To ", TextType.TEXT),
                TextNode("boldly", TextType.BOLD),
                TextNode(" go where ", TextType.TEXT),
                TextNode("Italians", TextType.ITALIC),
                TextNode(" have never ", TextType.TEXT),
                TextNode("coded before", TextType.CODE),
                TextNode(": ", TextType.TEXT),
                TextNode("Mt Vesuvius", TextType.IMAGE, "https://mtvesuvius.org/pompeii-python-coders"),
            ],
            new_nodes,
        )

    def test_split_text_t_i_t_b_t_l_t_b(self):
        s = "This is an image of "
        s += "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg), some **bold text**, and a link: "
        s += "[link](https://boot.dev) followed by **more bold text**"

        new_nodes = text_to_textnodes(s)
        self.assertListEqual(
            [
                TextNode("This is an image of ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(", some ", TextType.TEXT),                
                TextNode("bold text", TextType.BOLD),
                TextNode(", and a link: ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" followed by ", TextType.TEXT),
                TextNode("more bold text", TextType.BOLD),                
            ],
            new_nodes,
        )










if __name__ == "__main__":
    unittest.main()

