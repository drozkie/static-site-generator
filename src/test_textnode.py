import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        self.assertEqual(node, node2)

    def test_noteq_with_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_noteq_with_url_and_none(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_noteq_with_same_url_diff_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev/")
        node2 = TextNode("This is a text node", TextType.NORMAL, "https://www.boot.dev/")
        self.assertNotEqual(node, node2)

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "Hello World", [TextNode("Hello World", TextType.NORMAL)], {"class": "container"})
        node2 = HTMLNode("div", "Hello World", [TextNode("Hello World", TextType.NORMAL)], {"class": "container"})
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode("div", "Hello World", [TextNode("Hello World", TextType.NORMAL)], {"class": "container"})
        node2 = HTMLNode("div", "Hello World", [TextNode("Hello World", TextType.NORMAL)], {"class": "container-fluid"})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello World", [TextNode("Hello World", TextType.NORMAL)], {"class": "container"})
        self.assertEqual(node.props_to_html(), 'class="container"')

    def test_props_to_html_empty(self):
        node = HTMLNode("div", "Hello World", [TextNode("Hello World", TextType.NORMAL)], {})
        self.assertEqual(node.props_to_html(), '')

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()