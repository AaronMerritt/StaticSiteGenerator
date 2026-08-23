import os
import shutil
import sys
from generatepagesrecursive import generate_pages_recursive
from textnode import TextNode, TextType
from generatepage import generate_page

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)
    static_dir = "static"
    public_dir = "public"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)

    def copy_static_to_public(source, destination):
        for item in os.listdir(source):
            source_path = os.path.join(source, item)
            destination_path = os.path.join(destination, item)

            if os.path.isdir(source_path):
                os.makedirs(destination_path)
                copy_static_to_public(source_path, destination_path)
            else:
                shutil.copy(source_path, destination_path)

    copy_static_to_public(static_dir, public_dir)
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()