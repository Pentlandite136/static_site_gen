import re
from enum import Enum
from textnode import TextType, TextNode
from htmlnode import HTMLNode

class BlockType(Enum):
    NORMAL_PARAGRAPH = 1
    HEADING_BLOCK = 2
    CODE_BLOCK = 3
    QUOTE_BLOCK = 4
    UNORDERED_LIST_BLOCK = 5
    ORDERED_LIST_BLOCK = 6

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

def markdown_to_blocks(markdown: str) -> list[str]:
    new_block_list = []                                 # what will be returned;
    block_list = markdown.split("\n\n")                 # split well-written md string based on double-newline;
    for block in block_list:                            # get a block...
        if len(block) != 0:                             # is block non-empty?
            new_block = block.strip()                   # yes, so remove any whitespace (" ", "\t", "\n") from both ends;
            if len(new_block) != 0:                     # is result non-empty?
                new_block_list.append(new_block)        # yes, so append it to the new list;
    return new_block_list

def is_heading_block(markdown_block: str) -> bool:
    padded_block = markdown_block + "      "            # pad 6 trailing blanks so it is always long enough for slicing;
    for i in range(2, 8):                               # i is stop index (exclusive) for slicing;
        if padded_block[:i] == ("#" * (i - 1)) + " ":   # replicate '#' and attach trailing blank; match?
            return True                                 # valid heading block;
    return False                                        # something else

def is_code_block(markdown_block: str) -> bool:
    if len(markdown_block) < 7:                         # code block must be at least 7 chars long;
        return False
    if markdown_block[:4] == "```\n" and markdown_block[-3:] == "```":  # 3 backticks and newline at start & 3 backticks at end...
        return True                                     # delimit a code block
    else:
        return False

def is_quote_block(markdown_block: str) -> bool:
    line_list = markdown_block.split("\n")             # split md using newline char to get a list of lines;
    for line in line_list:                             # examine a line;
        if len(line) == 0:                             # an empty line 
            return False                               # does not meet quote block definition;
        elif line[0] != ">":                           # line has at least 1 char, so we can index; is 1st char other than ">" ?
            return False                               # yes, so not a quote block;
    return True                                        # all lines begin with ">"
 
def is_unordered_list_block(markdown_block) -> bool:
    line_list = markdown_block.split("\n")             # split md using newline char to get a list of lines;
    for line in line_list:                             # examine a line;
        if len(line) < 2:                              # an empty line or too short to contain "> "
            return False                               # does not meet unordered list block definition;
        elif line[:2] != "- ":                         # line has at least 2 chars, so we can index; are first 2 chars other than "- "?
            return False                               # yes, so not an unordered list block;
    return True                                        # all lines begin with "- "

def is_ordered_list_block(markdown_block) -> bool:
    list_number = 1                                    # 1st list number must be 1;
    line_list = markdown_block.split("\n")             # split md using newline char to get a list of lines;
    for line in line_list:                             # examine a line;
        if len(line) == 0:                             # an empty line
            return False                               # does not meet ordered list block definition;
        dot_space_list = line.split(". ", 1)           # try to split the line at ". " but only first split piece is relevant;
        pre_dot_space = dot_space_list[0]              # for clarity, this is the text preceding the ". ";
        if len(pre_dot_space) == 0:                    # nothing preceded the ". " so number is absent
            return False                               # thus malformed ordered list;
        try:
            number = int(pre_dot_space)                # try to convert substring before the ". " into an integer;
        except ValueError:                             # not a convertible integer, so 
            return False                               # malformed md
        if number == list_number:                      # is number sequential?
            list_number += 1                           # yes, so bump the next expected one
        else:                                          # no, so
            return False                               # this is a malformed ordered list;
    return True                                        # all lines numbered correctly
                                     

def block_to_block_type(markdown_block: str) -> BlockType:
    if len(markdown_block) == 0:
        return BlockType.NORMAL_PARAGRAPH
    elif is_heading_block(markdown_block):
        return BlockType.HEADING_BLOCK
    elif is_code_block(markdown_block):
        return BlockType.CODE_BLOCK
    elif is_quote_block(markdown_block):
        return BlockType.QUOTE_BLOCK
    elif is_unordered_list_block(markdown_block):
        return BlockType.UNORDERED_LIST_BLOCK
    elif is_ordered_list_block(markdown_block):
        return BlockType.ORDERED_LIST_BLOCK
    else:
        return BlockType.NORMAL_PARAGRAPH

def create_HTMLNode_for_paragraph_block(markdown_block: str) -> HTMLNode:
    no_newlines_block = markdown_block.replace("\n", " ")         # replace all newlines with a blank;
    tag = "p"                                                     # tag for paragraph;
    node = HTMLNode(tag, no_newlines_block)                       # build the node;
    return node

def create_HTMLNode_for_heading_block(markdown_block: str) -> HTMLNode:
    index_of_leftmost_blank = markdown_block.find(" ")             # md block is known to be a valid single heading block; find the " ";
    tag = f"h{index_of_leftmost_blank}"                            # heading level number is exactly the index of the blank; build the tag;
    node = HTMLNode(tag, markdown_block[index_of_leftmost_blank:]) # the found blank is part of the value; build HTML node
    return node

def create_HTMLNode_for_code_block(markdown_block: str) -> HTMLNode:
    index_of_leftmost_newline = markdown_block.find("\n")          # md block is known to be a valid code block; find the newline;
    index_start = index_of_leftmost_newline + 1                    # slice start is char after this newline;
    index_stop  = len(markdown_block) - 3                          # slice stop is 3 tickmarks before end;
    child_tag = "code"                                             # this code block is the child node, and
    value = markdown_block[index_start : index_stop]               # text in between is the value;
    child_node = HTMLNode(child_tag, value)                        # build child node;
    parent_tag = "pre"                                             # define parent tag;
    parent_node = HTMLNode(parent_tag, "", [child_node])           # build HTML parent node with a list of one child node;
    return parent_node

def create_HTMLNode_for_quote_block(markdown_block: str) -> HTMLNode:
    line_list = markdown_block.split("\n")                         # md block is known to be a valid quote block; split it into lines;
    new_line_str = ""                                              # init the new line list w/o leading ">";
    for line in line_list:                                         # process each line;
        quoted_line = line[1:] + "\n"                              # slice around ">" at index of 0 and re-attach a newline;
        new_line_str += quoted_line                                # build up the new string of lines 
    tag = "quoteblock"                                             # define the tag
    node = HTMLNode(tag, new_line_str)                             # build HTML node
    return node

def create_HTMLNode_for_unordered_list_block(markdown_block: str) -> HTMLNode:
    child_node_list = []                                           # init the list of children nodes;
    line_list = markdown_block.split("\n")                         # md block is known to be a valid unordered list block; split it into lines;
    child_tag = "li"                                               # tag each line item as a child node;
    for line_item in line_list:                                    # process each line item;
        tagged_line_item = line_item + "\n"                        # keep leading "- "; re-attach a newline;
        child_node = HTMLNode(child_tag, tagged_line_item)         # build HTML child node from this line item;
        child_node_list.append(child_node)                         # append child node to the list of children nodes;
    parent_tag = "ul"                                              # parent node is an unordered list;
    parent_node = HTMLNode(parent_tag, "", child_node_list)        # build the parent node & include the list of children nodes         
    return parent_node

def create_HTMLNode_for_ordered_list_block(markdown_block: str) -> HTMLNode:
    child_node_list = []                                           # init the list of children nodes;
    line_list = markdown_block.split("\n")                         # md block is known to be a valid ordered list block; split it into lines;
    child_tag = "li"                                               # tag each line item as a child node;
    for line_item in line_list:                                    # process each line item;
        tagged_line_item = line_item + "\n"                        # keep ordered list number and dot; re-attach a newline;
        child_node = HTMLNode(child_tag, tagged_line_item)         # build HTML line item node;
        child_node_list.append(child_node)                         # append to the list of children nodes
    parent_tag = "ol"                                              # parent node is an ordered list
    parent_node = HTMLNode(parent_tag, "", child_node_list)        # build the parent node & include the list of children nodes         
    return parent_node






def markdown_to_html(markdown: str) -> HTMLNode:
    list_of_blocks = markdown_to_blocks(markdown)             # split md into list of blocks;
    for block in list_of_blocks:                              # examine a block
        match block_to_block_type(block):                     # & determine what type of block it is;
            case BlockType.NORMAL_PARAGRAPH:
                pass
            case BlockType.HEADING_BLOCK:
                node = create_HTMLNode_for_heading_block(markdown)
            case BlockType.CODE_BLOCK:
                node = create_HTMLNode_for_code_block(markdown)
            case BlockType.QUOTE_BLOCK:
                node = create_HTMLNode_for_quote_block(markdown)
            case BlockType.UNORDERED_LIST_BLOCK:
                node = create_HTMLNode_for_unordered_list_block(markdown)
            case BlockType.ORDERED_LIST_BLOCK:
                node = create_HTMLNode_for_ordered_list_block(markdown)
            case _:
                raise Exception(f"Error: unidentified block type")

    


     