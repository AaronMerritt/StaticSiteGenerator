import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        node5 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node6 = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node7 = TextNode("This is a text node", TextType.CODETEXT)
        node8 = TextNode("This is a text node", TextType.CODETEXT)
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertEqual(node5, node6)
        self.assertEqual(node7, node8)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD)
        node5 = TextNode("This is a text node", TextType.LINK)
        node6 = TextNode("This is a text node", TextType.BOLD)
        node7 = TextNode("This is a text node", TextType.ITALIC)
        node8 = TextNode("This is a text node", TextType.CODETEXT)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node5, node6)
        self.assertNotEqual(node7, node8)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code text", TextType.CODETEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("This is alt text", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-150.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev/img/bootdev-logo-full-150.png", "alt": "This is alt text"},
        )

    def test_invalid_type_raises(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        node.text_type = "not_a_real_type"
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()