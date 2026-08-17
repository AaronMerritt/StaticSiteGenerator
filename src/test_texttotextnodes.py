import unittest
from textnode import TextNode, TextType
from texttotextnodes import text_to_textnodes


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text with no markdown"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("This is plain text with no markdown", TextType.PLAIN)], new_nodes
        )

    def test_bold(self):
        text = "This is text with a **bolded phrase** in the middle"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_italic(self):
        text = "This is text with an _italic phrase_ in the middle"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" in the middle", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_codetext(self):
        text = "This is text with a `code block` in the middle"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODETEXT),
                TextNode(" in the middle", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_link(self):
        text = "This is text with a [link](https://www.boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_all_node_types_together(self):
        text = (
            "This is **bold** text with an _italic_ word, a `code block`, an "
            "![image](https://i.imgur.com/zjjcJKZ.png), and a [link](https://boot.dev)"
        )
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("bold", TextType.BOLD),
                TextNode(" text with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word, a ", TextType.PLAIN),
                TextNode("code block", TextType.CODETEXT),
                TextNode(", an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(", and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_multiple_images_and_links(self):
        text = (
            "![one](https://i.imgur.com/1.png) and [two](https://www.boot.dev) "
            "and ![three](https://i.imgur.com/3.png)"
        )
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://i.imgur.com/1.png"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("two", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("three", TextType.IMAGE, "https://i.imgur.com/3.png"),
            ],
            new_nodes,
        )

    def test_no_markdown_is_single_plain_node(self):
        text = "Just some words."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("Just some words.", TextType.PLAIN)], new_nodes)


if __name__ == "__main__":
    unittest.main()
