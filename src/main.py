from textnode import *
from htmlnode import *
from markdown import *
from blocks import *
import re

def main():
    pass

def assign_html_node(blocks):
    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.PARAGRAPH:
                html_nodes.append(HTMLNode("p", block))
            case BlockType.HEADING:
                heading = re.match(r"/^(\#{1,6})/g", block)
                count = len(heading)
                html_nodes.append(HTMLNode(f"h{count}", block))
            case BlockType.QUOTE:
                html_nodes.append(HTMLNode("q", block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(HTMLNode("ul", block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(HTMLNode("ol", block))
    return html_nodes

def convert_markdown(text):
    ## Convert Text to Blocks
    blocks = markdown_to_blocks(text)

    ## Create HTMLNode Equivalent
    html_nodes = assign_html_node(blocks)

    ##

#Loop over each block
##Determine the type of block (you already have a function for this)
##Based on the type of block, create a new HTMLNode with the proper data
##Assign the proper child HTMLNode objects to the block node. I created a shared text_to_children(text) function that works for all block types. It takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (think TextNode -> HTMLNode).
##The "code" block is a bit of a special case: it should not do any inline markdown parsing of its children. I didn't use my text_to_children function for this block type, I manually made a TextNode and used text_node_to_html_node.

#Make all the block nodes children under a single parent HTML node (which should just be a div) and return it.
#Create unit tests.

main()