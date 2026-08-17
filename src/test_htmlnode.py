import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Some text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "Some text", None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_values(self):
        node = HTMLNode("div", "Hello", None, {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.props, {"class": "container"})

    def test_repr(self):
        node = HTMLNode("p", "text")
        self.assertIn("HTMLNode", repr(node))

if __name__ == "__main__":
    unittest.main()
