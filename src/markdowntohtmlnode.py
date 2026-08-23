from htmlnode import HTMLNode
from parentnode import ParentNode
from markdowntoblocks import markdown_to_blocks
from blocktype import BlockType, block_to_block_type
from textnode import TextNode, TextType, text_node_to_html_node
from texttotextnodes import text_to_textnodes


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


def paragraph_to_html_node(block: str) -> HTMLNode:
    paragraph = " ".join(block.split("\n"))
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> HTMLNode:
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> HTMLNode:
    text = block[4:-3]
    text_node = TextNode(text, TextType.PLAIN)
    code_leaf = text_node_to_html_node(text_node)
    code_node = ParentNode("code", [code_leaf])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    list_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    list_items = []
    for item in items:
        text = item.split(". ", 1)[1]
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"Invalid block type: {block_type}")


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return ParentNode("div", children)
