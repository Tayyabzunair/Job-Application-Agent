"""
Ingests the resume PDF into a ChromaDB knowledge base.
Run once — re-run whenever you update your resume.
"""
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from src.config import CHROMA_DIR

RESUME_PDF = "data/master_resume.pdf"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # free, fast, local


def extract_pdf_text(pdf_path: str) -> str:
    """Extracts text from all pages of the PDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def ingest_resume():
    print("Reading resume PDF...")
    raw_text = extract_pdf_text(RESUME_PDF)

    if not raw_text.strip():
        raise ValueError("No text extracted from PDF! Please check the file.")

    print(f"Extracted {len(raw_text)} characters.")

    # Split text into overlapping chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_text(raw_text)
    print(f"Created {len(chunks)} chunks.")

    # Free local embeddings
    print("Loading embeddings model (downloads on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # Store in ChromaDB
    print("Storing in ChromaDB...")
    Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name="resume",
    )

    print(f"Done! Knowledge base saved in '{CHROMA_DIR}'.")


if __name__ == "__main__":
    ingest_resume()
