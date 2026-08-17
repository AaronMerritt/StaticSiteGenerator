import unittest
from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODETEXT)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("code block", TextType.CODETEXT),
                TextNode(" word", TextType.PLAIN),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.PLAIN),
            ],
        )

    def test_italic(self):
        node = TextNode("This is text with an _italic word_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("italic word", TextType.ITALIC),
            ],
        )

    def test_multiple_delimiters(self):
        node = TextNode("**bold** and **more bold**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.PLAIN),
                TextNode("more bold", TextType.BOLD),
            ],
        )

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`code`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODETEXT)
        self.assertEqual(new_nodes, [TextNode("code", TextType.CODETEXT)])

    def test_no_delimiter_present(self):
        node = TextNode("This is plain text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODETEXT)
        self.assertEqual(new_nodes, [TextNode("This is plain text", TextType.PLAIN)])

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("already bold", TextType.BOLD)])

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This has an unmatched ` delimiter", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODETEXT)

    def test_multiple_old_nodes(self):
        nodes = [
            TextNode("text with `code`", TextType.PLAIN),
            TextNode("already italic", TextType.ITALIC),
            TextNode("more `code` here", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODETEXT)
        self.assertEqual(
            new_nodes,
            [
                TextNode("text with ", TextType.PLAIN),
                TextNode("code", TextType.CODETEXT),
                TextNode("already italic", TextType.ITALIC),
                TextNode("more ", TextType.PLAIN),
                TextNode("code", TextType.CODETEXT),
                TextNode(" here", TextType.PLAIN),
            ],
        )


if __name__ == "__main__":
    unittest.main()
