from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter
from splitimagelink import split_nodes_image, split_nodes_link

def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.PLAIN)]
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODETEXT)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes