import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_tag(self):
        node = LeafNode(None, "No tags.")
        self.assertEqual(node.to_html(), "No tags.")

class TestParentNode(unittest.TestCase):
    def test_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_no_tag(self):
        node = ParentNode(
            "",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        node2 = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            )
        with self.assertRaises(ValueError):
            node.to_html()
            node2.to_html()

    def test_no_children(self):
        node = ParentNode(
            "p",
            None,
            )
        node2 = ParentNode(
            None,
            [],
            )
        with self.assertRaises(ValueError):
            node.to_html()
            node2.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()