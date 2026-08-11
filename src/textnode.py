from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = 0
    BOLD_TEXT = 1
    ITALIC_TEXT  = 2
    CODE_TEXT = 3
    LINK_TEXT = 4
    IMAGE_TEXT = 5

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url if text_type == TextType.LINK_TEXT or text_type == TextType.IMAGE_TEXT else None

    def __eq__ (self, other: TextNode) -> bool:
        result1 = self.text == other.text
        result2 = self.text_type == other.text_type
        result3 = self.url == other.url
        return result1 and result2 and result3

    def __repr__(self) -> str:
        class_name = type(self).__name__
        result = f"{class_name}({self.text!r}, {self.text_type.name!r}, {self.url!r})" 
        return result


