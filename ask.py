import sys
from google import genai
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-small")
collection = chromadb.PersistentClient(path="db").get_collection("docs")
client = genai.Client()  # διαβάζει το GEMINI_API_KEY

SYSTEM = (
    "Είσαι βοηθός που απαντά ερωτήσεις για τον Κώδικα Οδικής Κυκλοφορίας "
    "(έκδοση 2007). Απάντα ΜΟΝΟ με βάση τα αποσπάσματα που σου δίνονται και "
    "ανέφερε τη σελίδα. Αν η απάντηση δεν υπάρχει στα αποσπάσματα, πες το "
    "καθαρά. Ο ΚΟΚ έχει τροποποιηθεί από το 2007, οπότε η απάντηση δεν "
    "αποτελεί νομική συμβουλή."
)

def retrieve(question, k=8):
    emb = model.encode(["query: " + question]).tolist()
    res = collection.query(query_embeddings=emb, n_results=k)
    return list(zip(res["documents"][0], res["metadatas"][0]))

def answer(question):
    hits = retrieve(question)
    context = "\n\n".join(f"[Σελίδα {m['page']}]\n{d}" for d, m in hits)
    resp = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=f"Αποσπάσματα:\n{context}\n\nΕρώτηση: {question}",
        config={"system_instruction": SYSTEM},
    )
    return resp.text, hits

if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or input("Ερώτηση: ")
    text, hits = answer(q)
    print(text)
    print("\nΠηγές: σελίδες", sorted({m["page"] for _, m in hits}))