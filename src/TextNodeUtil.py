import re
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
                           
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
        
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []                                # to be returned;
    for old_node in old_nodes:                    # grab a node from the input list;
        if old_node.text_type != TextType.TEXT:   # if a non-TEXT node, 
            new_nodes.append(old_node)            # simply add to new node list and move on;
        else:                                     # this is a TEXT node so
            my_string = old_node.text             # set its text element as the string to be searched;        
            images_list = extract_markdown_images(my_string)     # build list of all images in this string;
            if len(images_list) == 0:                            # no image(s) found?
                new_nodes.append(old_node)                       # then attach it to new node list & move on.
            else:                                                # at least one image was found; 
                for image_tuple in images_list:                  # process each found image stored as a tuple;
                    image_text = image_tuple[0]                  # for visual clarity;
                    image_url  = image_tuple[1]                  # ditto;

                    delimiter = f"![{image_text}]({image_url})"  # construct the l-o-n-g delimiter &
                    split_list = my_string.split(delimiter, 1)   # split the string using it;
                    if len(split_list) != 2:                     # should always produce list of 2 elements, but if not
                        raise Exception("Error: len(split_list) is not 2")  # say so;
                    
                    pre_image_text = split_list[0]               # the TEXT before the image;
                    post_image_text = split_list[1]              # the TEXT after the image;

                    if len(pre_image_text) != 0:                 # if there is some pre image text
                        pre_text_node = TextNode(pre_image_text, TextType.TEXT) # build a new TEXT node for it &
                        new_nodes.append(pre_text_node)          # include it in new list;

                    image_node = TextNode(image_text, TextType.IMAGE, image_url)  # create the new IMAGE node &                      
                    new_nodes.append(image_node)                 # include it in new list;

                    my_string = post_image_text                  # search for more images only in the REMAINING piece of string

                if len(my_string) != 0:                                 # if a residual string exists after all images processed,
                    post_text_node = TextNode(my_string, TextType.TEXT) # then it must be TEXT, so build a TEXT node &
                    new_nodes.append(post_text_node)                    # attach as final new node element

    return new_nodes    

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []                                # to be returned;
    for old_node in old_nodes:                    # grab a node from the input list;
        if old_node.text_type != TextType.TEXT:   # if a non-TEXT node, 
            new_nodes.append(old_node)            # simply add to new node list and move on;
        else:                                     # this is a TEXT node so
            my_string = old_node.text             # set its text element as the string to be searched;        
            links_list = extract_markdown_links(my_string)       # build list of all links in this string;
            if len(links_list) == 0:                             # no link(s) found?
                new_nodes.append(old_node)                       # then attach it to new node list & move on.
            else:                                                # at least one link was found; 
                for link_tuple in links_list:                    # process each found link stored as a tuple;
                    link_text = link_tuple[0]                    # for visual clarity;
                    link_url  = link_tuple[1]                    # ditto;

                    delimiter = f"[{link_text}]({link_url})"     # construct the l-o-n-g delimiter &
                    split_list = my_string.split(delimiter, 1)   # split the string using it;
                    if len(split_list) != 2:                     # should always produce list of 2 elements, but if not
                        raise Exception("Error: len(split_list) is not 2")  # say so;
                    
                    pre_link_text  = split_list[0]               # the TEXT before the link;
                    post_link_text = split_list[1]               # the TEXT after the link;

                    if len(pre_link_text) != 0:                  # if there is some pre link text
                        pre_text_node = TextNode(pre_link_text, TextType.TEXT) # build a new TEXT node for it &
                        new_nodes.append(pre_text_node)          # include it in new list;

                    link_node = TextNode(link_text, TextType.LINK, link_url)  # create the new LINK node &                      
                    new_nodes.append(link_node)                  # include it in new list;
                    
                    my_string = post_link_text                   # search for more links only in the REMAINING piece of string

                if len(my_string) != 0:                                 # if a residual string exists after all links processed,
                    post_text_node = TextNode(my_string, TextType.TEXT) # then it must be TEXT, so build a TEXT node &
                    new_nodes.append(post_text_node)                    # attach as final new node element

    return new_nodes 

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes0 = [TextNode(text, TextType.TEXT)]
    nodes1 = split_nodes_delimiter(nodes0, "`", TextType.CODE)
    nodes2 = split_nodes_delimiter(nodes1, "**", TextType.BOLD)
    nodes3 = split_nodes_delimiter(nodes2, "_", TextType.ITALIC)
    nodes4 = split_nodes_image(nodes3)
    nodes5 = split_nodes_link(nodes4)

    return nodes5







     