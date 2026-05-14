import io
import pypdf
from docx import Document

def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Extracts raw text from PDF, DOCX, or TXT files.
    """
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )

    elif ext == "docx":
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join(para.text for para in doc.paragraphs)

    elif ext == "txt":
        text = file_bytes.decode("utf-8")

    else:
        raise ValueError(f"Unsupported file type: .{ext}")

    if not text.strip():
        raise ValueError(
            f"Could not extract text from {filename}. "
            f"File may be scanned or image-based."
        )

    return text.strip()