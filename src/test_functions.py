import unittest

from functions import *
from textnode import *
from htmlnode import *

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link(self):
        node = TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Boot.dev")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})
        self.assertEqual(html_node.to_html(), '<a href="https://www.boot.dev">Boot.dev</a>')

    def test_image(self):
        node = TextNode("Boot.dev", TextType.IMAGE, "images/boot_test_image.gif")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"alt": "Boot.dev", "src": "images/boot_test_image.gif"})
        self.assertEqual(html_node.to_html(), '<img src="images/boot_test_image.gif" alt="Boot.dev">')

class TestTextToHTMLNode(unittest.TestCase):
    def test_split_text(self):
        node = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(len(split_node), 3)
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[0].text, "This is text with a ")
        self.assertEqual(split_node[1].text_type, TextType.CODE)
        self.assertEqual(split_node[1].text, "code block")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[2].text, " word")

    def test_split_text_two_nodes(self):
        node = [TextNode("This is text with a `code block` word", TextType.TEXT), TextNode("This is another text with a `bigger code block` word", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(len(split_node), 6)
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[0].text, "This is text with a ")
        self.assertEqual(split_node[1].text_type, TextType.CODE)
        self.assertEqual(split_node[1].text, "code block")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[2].text, " word")
        self.assertEqual(split_node[3].text_type, TextType.TEXT)
        self.assertEqual(split_node[3].text, "This is another text with a ")
        self.assertEqual(split_node[4].text_type, TextType.CODE)
        self.assertEqual(split_node[4].text, "bigger code block")
        self.assertEqual(split_node[5].text_type, TextType.TEXT)
        self.assertEqual(split_node[5].text, " word")

    def test_split_bold(self):
        node = [TextNode("This is text with a **bold** word", TextType.TEXT)]
        split_node = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(len(split_node), 3)
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[0].text, "This is text with a ")
        self.assertEqual(split_node[1].text_type, TextType.BOLD)
        self.assertEqual(split_node[1].text, "bold")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[2].text, " word")

    def test_split_image(self):
        node = [TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and some text.", TextType.TEXT)]
        split_node = split_nodes_image(node)
        self.assertEqual(len(split_node), 3)
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[0].text, "This is text with an ")
        self.assertEqual(split_node[1].text_type, TextType.IMAGE)
        self.assertEqual(split_node[1].text, "image")
        self.assertEqual(split_node[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[2].text, " and some text.")

    def test_split_link(self):
        node = [TextNode("This is text with a [drozkie.net](https://www.drozkie.net) and some text.", TextType.TEXT)]
        split_node = split_nodes_link(node)
        self.assertEqual(len(split_node), 3)
        self.assertEqual(split_node[0].text_type, TextType.TEXT)
        self.assertEqual(split_node[0].text, "This is text with a ")
        self.assertEqual(split_node[1].text_type, TextType.LINK)
        self.assertEqual(split_node[1].text, "drozkie.net")
        self.assertEqual(split_node[1].url, "https://www.drozkie.net")
        self.assertEqual(split_node[2].text_type, TextType.TEXT)
        self.assertEqual(split_node[2].text, " and some text.")

class MarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) [link-text](https://www.boot.dev)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link-text](https://www.boot.dev)"
        )
        self.assertListEqual([("link-text", "https://www.boot.dev")], matches)

if __name__ == "__main__":
    unittest.main()