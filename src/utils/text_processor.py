import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """Mengekstrak teks dari PDF menggunakan PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def clean_legal_text(text):
    """Pembersihan dasar untuk teks hukum."""
    # Hapus nomor halaman
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    # Gabungkan baris yang terputus
    text = re.sub(r'([a-z])\n([a-z])', r'\1 \2', text)
    # Hapus whitespace berlebih
    text = re.sub(r' +', ' ', text)
    return text.strip()

def chunk_text(text, chunk_size=1000):
    """Memecah teks menjadi potongan (chunks) berdasarkan paragraf."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for p in paragraphs:
        if len(current_chunk) + len(p) < chunk_size:
            current_chunk += p + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = p + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks