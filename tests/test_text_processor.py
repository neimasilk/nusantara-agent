import unittest
from unittest.mock import MagicMock, patch
from src.utils.text_processor import clean_legal_text, chunk_text, extract_text_from_pdf

class TextProcessorTests(unittest.TestCase):
    def test_clean_legal_text_basic(self):
        text = "Pasal 1\n\n  123  \n\nIsi pasal."
        cleaned = clean_legal_text(text)
        self.assertIn("Pasal 1", cleaned)
        self.assertIn("Isi pasal.", cleaned)
        # Check if page number "123" surrounded by newlines is removed
        self.assertNotIn("\n  123  \n", cleaned)

    def test_clean_legal_text_broken_lines(self):
        text = "Hukum nasion\nal lebih tinggi\ndari adat."
        cleaned = clean_legal_text(text)
        # Current logic joins with space: re.sub(r'([a-z])\n([a-z])', r'\1 \2', text)
        self.assertEqual(cleaned, "Hukum nasion al lebih tinggi dari adat.")

    def test_clean_legal_text_whitespace(self):
        text = "Banyak    spasi  dan \n  baris baru."
        cleaned = clean_legal_text(text)
        # Should replace multiple spaces with single space
        self.assertIn("Banyak spasi dan", cleaned)
        self.assertIn("baris baru.", cleaned)

    def test_clean_legal_text_empty(self):
        """Edge case: empty string should return empty string."""
        self.assertEqual(clean_legal_text(""), "")
        self.assertEqual(clean_legal_text("   "), "")

    def test_chunk_text_basic(self):
        text = "Paragraf satu.\n\nParagraf dua.\n\nParagraf tiga."
        # chunk_size=30: 
        # "Paragraf satu." (14) + "Paragraf dua." (13) = 27 < 30.
        # They will be in the same chunk.
        chunks = chunk_text(text, chunk_size=30)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], "Paragraf satu.\n\nParagraf dua.")
        self.assertEqual(chunks[1], "Paragraf tiga.")

    def test_chunk_text_no_split_needed(self):
        text = "Satu paragraf pendek."
        chunks = chunk_text(text, chunk_size=100)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], "Satu paragraf pendek.")

    def test_chunk_text_empty(self):
        """Edge case: empty text should return empty list."""
        result = chunk_text("")
        self.assertEqual(result, [])

    def test_chunk_text_boundary(self):
        """Edge case: exactly at chunk_size boundary."""
        text = "AAAAA\n\nBBBBB" # length 12
        chunks = chunk_text(text, chunk_size=6)
        # "AAAAA" is 5 chars. "AAAAA\n\n" would be 7. 
        # So "AAAAA" fits in first chunk. "BBBBB" in second.
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], "AAAAA")
        self.assertEqual(chunks[1], "BBBBB")

    @patch("fitz.open")
    def test_extract_text_from_pdf_empty(self, mock_open):
        """Edge case: empty PDF extraction."""
        mock_doc = MagicMock()
        mock_doc.__iter__.return_value = [] # No pages
        mock_open.return_value = mock_doc
        
        result = extract_text_from_pdf("dummy.pdf")
        self.assertEqual(result, "")

    @patch("fitz.open")
    def test_extract_text_from_pdf_content(self, mock_open):
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Halaman 1"
        mock_doc = MagicMock()
        mock_doc.__iter__.return_value = [mock_page]
        mock_open.return_value = mock_doc
        
        result = extract_text_from_pdf("dummy.pdf")
        self.assertEqual(result, "Halaman 1")

if __name__ == "__main__":
    unittest.main()
