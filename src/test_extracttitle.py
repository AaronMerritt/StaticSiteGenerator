import unittest
from extracttitle import extract_title

class TestExtractTitle(unittest.TestCase):
	def test_extract_title(self):
		markdown = "# My Title"
		self.assertEqual(extract_title(markdown), "My Title")

	def test_extract_title_with_whitespace(self):
		markdown = "# My Title   "
		self.assertEqual(extract_title(markdown), "My Title")

	def test_extract_title_with_no_space(self):
		markdown = "#My Title"
		self.assertEqual(extract_title(markdown), "My Title")

	def test_extract_title_not_found(self):
		markdown = "## My Title"
		with self.assertRaises(ValueError):
			extract_title(markdown)

if __name__ == "__main__":
	unittest.main()