import os
from extracttitle import extract_title
from markdowntohtmlnode import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
	template = open(template_path, "r", encoding="utf-8").read()

	for dirpath, dirnames, filenames in os.walk(dir_path_content):
		for filename in filenames:
			if not filename.endswith(".md"):
				continue

			source_path = os.path.join(dirpath, filename)
			relative_path = os.path.relpath(source_path, dir_path_content)
			destination_path = os.path.join(
				dest_dir_path, os.path.splitext(relative_path)[0] + ".html"
			)

			with open(source_path, "r", encoding="utf-8") as markdown_file:
				markdown = markdown_file.read()

			html_node = markdown_to_html_node(markdown)
			title = extract_title(markdown)

			page = template.replace("{{ Title }}", title).replace(
				"{{ Content }}", html_node.to_html()
			)
			page = page.replace('href="/"', f'href="{basepath}"').replace(
				'src="/"', f'src="{basepath}"'
			)
			os.makedirs(os.path.dirname(destination_path), exist_ok=True)
			with open(destination_path, "w", encoding="utf-8") as output_file:
				output_file.write(page)
