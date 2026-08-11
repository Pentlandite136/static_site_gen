from textnode import TextType
from textnode import TextNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(repr(text_node))

main()