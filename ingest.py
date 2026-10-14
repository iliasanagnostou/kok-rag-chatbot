import re
from pathlib import Path
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

CHUNK_SIZE = 800
OVERLAP = 150

# Το PDF έχει λατινικά γράμματα που μοιάζουν με ελληνικά (π.χ. o, P, H)
LOOKALIKES = str.maketrans({
    "A": "Α", "B": "Β", "E": "Ε", "Z": "Ζ", "H": "Η", "I": "Ι", "K": "Κ",
    "M": "Μ", "N": "Ν", "O": "Ο", "P": "Ρ", "T": "Τ", "Y": "Υ", "X": "Χ",
    "o": "ο",
})
GREEK = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]")
WORD = re.compile(r"[A-Za-z\u0370-\u03FF\u1F00-\u1FFF]+")

def fix_letters(text):
    def repl(m):
        w = m.group(0)
        return w.translate(LOOKALIKES) if GREEK.search(w) else w
    return WORD.sub(repl, text)

def chunk_text(text):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + CHUNK_SIZE])
        start += CHUNK_SIZE - OVERLAP
    return chunks

model = SentenceTransformer("intfloat/multilingual-e5-small")
client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("docs")

for pdf_path in Path("docs").glob("*.pdf"):
    reader = PdfReader(pdf_path)
    total = len(reader.pages)
    for page_num, page in enumerate(reader.pages, start=1):
        text = fix_letters((page.extract_text() or "").strip())
        chunks = chunk_text(text)
        if not chunks:
            continue
        embeddings = model.encode(["passage: " + c for c in chunks]).tolist()
        collection.add(
            ids=[f"{pdf_path.name}-p{page_num}-c{i}" for i in range(len(chunks))],
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{"source": pdf_path.name, "page": page_num}] * len(chunks),
        )
        print(f"Σελίδα {page_num}/{total}")
    print(f"Τέλος: {pdf_path.name}")