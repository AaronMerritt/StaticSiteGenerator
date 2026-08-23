import os
from extracttitle import extract_title
from markdowntohtmlnode import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath):
	print(
		f"Generating page from {from_path} to {dest_path} using {template_path}"
	)

	with open(from_path, "r", encoding="utf-8") as markdown_file:
		markdown = markdown_file.read()

	with open(template_path, "r", encoding="utf-8") as template_file:
		template = template_file.read()

	html = markdown_to_html_node(markdown).to_html()
	title = extract_title(markdown)
	full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
	full_html = full_html.replace('href="/"', f'href="{basepath}"').replace(
		'src="/"', f'src="{basepath}"'
	)

	os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
	with open(dest_path, "w", encoding="utf-8") as destination_file:
		destination_file.write(full_html)