from src.ingestion import extract_pdf
from src.chunking import create_chunks
from src.embeddings import model, generate_embeddings

from src.vector_store import (
    create_vector_store,
    search_vectors
)

pages=extract_pdf(
    "data/documents/employee-agreement.pdf"
)

chunks=create_chunks(pages)

embeddings=generate_embeddings(chunks)

index=create_vector_store(embeddings)

print("Total vectors stored: ",index.ntotal)

query="What is the notice period for resignation?"

query_embedding=model.encode([query])

distances, indices=search_vectors(
    index,
    query_embedding,
    k=3
)

print("\nRelevant Chunks:\n")

for distance, idx in zip(distances, indices):

    if idx == -1:
        continue

    print("Chunk ID:", chunks[idx]["chunk_id"])
    print("Page:", chunks[idx]["page_number"])
    print("Distance:", distance)
    print("Text:", chunks[idx]["text"])
    print("-" * 50)