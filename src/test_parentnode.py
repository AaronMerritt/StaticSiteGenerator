import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
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

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("b", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_to_html_with_props(self):
        node = ParentNode(
            "a",
            [LeafNode(None, "click me")],
            {"href": "https://boot.dev"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev">click me</a>',
        )

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "div",
                    [
                        ParentNode(
                            "span",
                            [LeafNode("b", "deep")],
                        )
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><div><span><b>deep</b></span></div></div>",
        )

    def test_to_html_multiple_parent_children(self):
        node = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "item1")]),
                ParentNode("li", [LeafNode(None, "item2")]),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li>item1</li><li>item2</li></ul>",
        )

    def test_repr(self):
        node = ParentNode("div", [LeafNode("b", "text")])
        self.assertIn("ParentNode", repr(node))

if __name__ == "__main__":
    unittest.main()
