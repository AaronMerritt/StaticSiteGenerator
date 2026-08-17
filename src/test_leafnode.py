import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just raw text")
        self.assertEqual(node.to_html(), "Just raw text")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Some span text")
        self.assertEqual(node.to_html(), "<span>Some span text</span>")

    def test_leaf_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_children(self):
        node = LeafNode("p", "text")
        self.assertIsNone(node.children)

    def test_repr(self):
        node = LeafNode("p", "text")
        self.assertIn("LeafNode", repr(node))
        self.assertNotIn("children", repr(node))

if __name__ == "__main__":
    unittest.main()
