from textnode import *
from htmlnode import *

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

def main():
    pass

main()