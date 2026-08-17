import unittest
from textnode import TextNode, TextType
from splitimagelink import split_nodes_image, split_nodes_link


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) starts the text",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" starts the text", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_image_is_entire_text(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")],
            new_nodes,
        )

    def test_adjacent_images_no_text_between(self):
        node = TextNode(
            "![one](https://i.imgur.com/1.png)![two](https://i.imgur.com/2.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.IMAGE, "https://i.imgur.com/1.png"),
                TextNode("two", TextType.IMAGE, "https://i.imgur.com/2.png"),
            ],
            new_nodes,
        )

    def test_no_images_present(self):
        node = TextNode("This is plain text with no images", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is plain text with no images", TextType.PLAIN)], new_nodes)

    def test_empty_alt_text(self):
        node = TextNode("Look: ![](https://i.imgur.com/blank.png) done", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Look: ", TextType.PLAIN),
                TextNode("", TextType.IMAGE, "https://i.imgur.com/blank.png"),
                TextNode(" done", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_non_plain_node_unchanged(self):
        node = TextNode("already a link", TextType.LINK, "https://www.boot.dev")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("already a link", TextType.LINK, "https://www.boot.dev")], new_nodes)

    def test_ignores_plain_links(self):
        node = TextNode("This is a [link](https://www.boot.dev), not an image", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("This is a [link](https://www.boot.dev), not an image", TextType.PLAIN)], new_nodes
        )

    def test_multiple_old_nodes(self):
        nodes = [
            TextNode("An ![img](https://i.imgur.com/1.png) here", TextType.PLAIN),
            TextNode("already bold", TextType.BOLD),
            TextNode("Another ![img2](https://i.imgur.com/2.png) there", TextType.PLAIN),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("An ", TextType.PLAIN),
                TextNode("img", TextType.IMAGE, "https://i.imgur.com/1.png"),
                TextNode(" here", TextType.PLAIN),
                TextNode("already bold", TextType.BOLD),
                TextNode("Another ", TextType.PLAIN),
                TextNode("img2", TextType.IMAGE, "https://i.imgur.com/2.png"),
                TextNode(" there", TextType.PLAIN),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_single_link(self):
        node = TextNode("Check [this out](https://www.boot.dev)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check ", TextType.PLAIN),
                TextNode("this out", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode("Go here: [boot dev](https://www.boot.dev)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Go here: ", TextType.PLAIN),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_link_is_entire_text(self):
        node = TextNode("[boot dev](https://www.boot.dev)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("boot dev", TextType.LINK, "https://www.boot.dev")], new_nodes)

    def test_adjacent_links_no_text_between(self):
        node = TextNode("[one](https://www.one.com)[two](https://www.two.com)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("one", TextType.LINK, "https://www.one.com"),
                TextNode("two", TextType.LINK, "https://www.two.com"),
            ],
            new_nodes,
        )

    def test_no_links_present(self):
        node = TextNode("This is plain text with no links", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is plain text with no links", TextType.PLAIN)], new_nodes)

    def test_non_plain_node_unchanged(self):
        node = TextNode("already an image", TextType.IMAGE, "https://i.imgur.com/1.png")
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("already an image", TextType.IMAGE, "https://i.imgur.com/1.png")], new_nodes
        )

    def test_ignores_images(self):
        node = TextNode("This is an ![image](https://i.imgur.com/zjjcJKZ.png), not a link", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("This is an ![image](https://i.imgur.com/zjjcJKZ.png), not a link", TextType.PLAIN)],
            new_nodes,
        )

    def test_mixed_image_and_link(self):
        node = TextNode(
            "Here is a ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is a ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )

    def test_multiple_old_nodes(self):
        nodes = [
            TextNode("A [link](https://www.one.com) here", TextType.PLAIN),
            TextNode("already italic", TextType.ITALIC),
            TextNode("Another [link2](https://www.two.com) there", TextType.PLAIN),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("A ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.one.com"),
                TextNode(" here", TextType.PLAIN),
                TextNode("already italic", TextType.ITALIC),
                TextNode("Another ", TextType.PLAIN),
                TextNode("link2", TextType.LINK, "https://www.two.com"),
                TextNode(" there", TextType.PLAIN),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
