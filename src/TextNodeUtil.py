from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        my_string = old_node.text
        if old_node.text_type != TextType.TEXT or my_string == "":     # if non-TEXT or no text, simply add to new node list
            new_nodes.append(old_node)
        else:
            done = False 
            while not done:
                split_list = my_string.split(delimiter, 2)

                match len(split_list):
                    case 1:   # 1 part means delimiter not found in string
                        part = TextNode(my_string, TextType.TEXT)
                        if part.text != "":            # do not append a Node if there is no text
                            new_nodes.append(part)
                        done = True 
                    case 2:   # 2 parts means one instance of delimiter found in string
                        raise Exception(f"Error: MD delimiter '{delimiter}' not closed in string: '{my_string}'") 
                    case 3:   # 3 parts means two instances of delimiters found in string (so far ...)
                        part_1 = TextNode(split_list[0], TextType.TEXT)   # the part before the 1st delimiter is just TEXT
                        if part_1.text != "":           # do not append a Node if there is no text
                            new_nodes.append(part_1)
                        part_2 = TextNode(split_list[1], text_type)       # the middle part between delimiters becomes text_type
                        if part_2.text != "":                             # do not append a Node if there is no text
                            new_nodes.append(part_2)
                        my_string = split_list[2]

    return new_nodes
                           













     