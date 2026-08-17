from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid markdown: no closing delimiter found for '{delimiter}' in {old_node.text}"
            )

        split_nodes = []
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.PLAIN))
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)

    return new_nodes
