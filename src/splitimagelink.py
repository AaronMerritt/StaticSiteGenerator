from textnode import TextNode, TextType
from extractmarkdown import extract_markdown_images, extract_markdown_links


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        images = extract_markdown_images(remaining_text)
        if not images:
            new_nodes.append(old_node)
            continue

        for alt, url in images:
            prefix, remaining_text = remaining_text.split(f"![{alt}]({url})", 1)
            if prefix != "":
                new_nodes.append(TextNode(prefix, TextType.PLAIN))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue

        remaining_text = old_node.text
        links = extract_markdown_links(remaining_text)
        if not links:
            new_nodes.append(old_node)
            continue

        for anchor, url in links:
            prefix, remaining_text = remaining_text.split(f"[{anchor}]({url})", 1)
            if prefix != "":
                new_nodes.append(TextNode(prefix, TextType.PLAIN))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN))

    return new_nodes
