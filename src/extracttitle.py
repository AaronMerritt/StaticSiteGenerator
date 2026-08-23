def extract_title(markdown):
	for line in markdown.splitlines():
		if line.startswith("#") and not line.startswith("##"):
			return line[1:].strip()

	raise ValueError("Markdown does not contain an h1 header")
