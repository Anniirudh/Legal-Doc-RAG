from sentence_transformers import SentenceTransformer
from src.ingestion import extract_pdf
from src.chunking import create_chunks

model=SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(chunks):
    texts=[chunk["text"] for chunk in chunks]

    embeddings=model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    return embeddings

if __name__ == "__main__":

    pages=extract_pdf("data/documents/employee-agreement.pdf")

    chunks=create_chunks(pages)
    embeddings=generate_embeddings(chunks)

    print("Total chunks: ",len(chunks))
    print("Embedding shape: ",embeddings.shape)

    print("\nFirst embedding:")
    print(embeddings[0])
