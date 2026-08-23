from enum import Enum
from htmlnode import LeafNode     # need to import HTMLNode as well?

#def text_node_to_html_node(text_node: TextNode) -> LeafNode:
#       case TextType.TEXT:
#            return LeafNode(None, text_node.text)
#        case TextType.BOLD:
#            return LeafNode(tag="b", value=text_node.text)
#        case TextType.ITALIC:
#            return LeafNode(tag="i", value=text_node.text)
#        case TextType.CODE: 
#            return LeafNode(tag="code", value=text_node.text)
#        case TextType.LINK:
#            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
#        case TextType.IMAGE:
#            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": "alt text"})
#        case _:
#            raise Exception(f"Error: Invalid Enum case: {text_node.text_type}")


class TextType(Enum):
    TEXT = 0
    BOLD = 1
    ITALIC  = 2
    CODE = 3
    LINK = 4
    IMAGE = 5

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url if text_type == TextType.LINK or text_type == TextType.IMAGE else None

    def __eq__(self, other: TextNode) -> bool:
        result1 = self.text == other.text
        result2 = self.text_type == other.text_type
        result3 = self.url == other.url
        return result1 and result2 and result3

    def __ne__(self, other: TextNode) -> bool:
        result1 = self.text != other.text
        result2 = self.text_type != other.text_type
        result3 = self.url != other.url
        return result1 or result2 or result3       

    def __repr__(self) -> str:
        class_name = type(self).__name__
        result = f"{class_name}({self.text!r}, {self.text_type.name!r}, {self.url!r})" 
        return result

    def text_node_to_html_node(self) -> LeafNode:
        match self.text_type:
            case TextType.TEXT:
                return LeafNode(None, value=self.text)
            case TextType.BOLD:
                return LeafNode(tag="b", value=self.text)
            case TextType.ITALIC:
                return LeafNode(tag="i", value=self.text)
            case TextType.CODE: 
                return LeafNode(tag="code", value=self.text)
            case TextType.LINK:
                return LeafNode(tag="a", value=self.text, props={"href": self.url})
            case TextType.IMAGE:
                return LeafNode(tag="img", value="", props={"src": self.url, "alt": "alt text"})
            case _:
                raise Exception(f"Error: Invalid Enum case: {self.text_type}")




