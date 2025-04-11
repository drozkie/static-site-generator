from textnode import *
from htmlnode import *
import re

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches

## Untested below
def extract_markdown_bold(text):
    matches = re.findall(r"\*\*(.*?)\*\*", text)
    return matches

def extract_markdown_italic(text):
    matches = re.findall(r"\_(.*?)\_", text)
    return matches

def extract_markdown_code(text):
    matches = re.findall(r"\`(.*?)\`", text)
    return matches

## Untested above

### WORKING ON THIS FUNCTION NOW ###

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            split_node = node.text.split(delimiter, 3)
            if len(split_node) < 3:
                raise Exception(f"Closing delimiter not found.\nInput = {node}\nDelimiter = '{delimiter}'")
            new_nodes.extend(
                    [
                    TextNode(split_node[0], TextType.TEXT),
                    TextNode(split_node[1], text_type),
                    TextNode(split_node[2], TextType.TEXT)
                    ]
                )
        else:
            new_nodes.append(node)
    return new_nodes

def text_node_to_html_node(text_node):
    test_case = text_node.text_type
    match test_case:
        case test_case.NORMAL:
            return LeafNode(None, text_node.text)
        case test_case.BOLD:
            return LeafNode("b", text_node.text)
        case test_case.ITALIC:
            return LeafNode("i", text_node.text)
        case test_case.CODE:
            return LeafNode("code", text_node.text)
        case test_case.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case test_case.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError