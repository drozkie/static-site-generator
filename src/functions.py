from textnode import *
from htmlnode import *
import re

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    ### Iterate over old_nodes, check type, match regex, build new nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image in images:
            split_node = original_text.split(f"![{image[0]}]({image[1]})")

            if len(split_node) != 2:
                raise ValueError("Invalid image markdown.")

            if split_node[0] != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))

                new_nodes.append(
                    TextNode(
                        image[0],
                        TextType.IMAGE,
                        image[1]
                    )
                )
            original_text = split_node[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    ### Iterate over old_nodes, check type, match regex, build new nodes
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(node)

        for link in links:
            split_node = original_text.split(f"[{link[0]}]({link[1]})")

            if len(split_node) != 2:
                raise ValueError("Invalid link markdown.")

            if split_node[0] != "":
                new_nodes.append(TextNode(split_node[0], TextType.TEXT))

                new_nodes.append(
                    TextNode(
                        link[0],
                        TextType.LINK,
                        link[1]
                    )
                )
            original_text = split_node[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT and delimiter in node.text:
            split_node = node.text.split(delimiter, 2)
            if len(split_node) < 3:
                raise Exception(f"Closing delimiter not found.\nInput = {node}\nDelimiter = '{delimiter}'")
### NEEDS TO BE REDONE, CAUSING DUPLICATES IN LONG NODES
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

def text_to_text_node(text):
    if text == "":
        raise ValueError("Invalid value, string cannot be empty")
    if not isinstance(text, str):
        raise TypeError("Invalid input, not of type str")

    new_nodes = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)

    print(f"Printing Nodes: {new_nodes}")
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