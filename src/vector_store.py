import faiss
import numpy as np

def create_vector_store(embeddings):
    dimension=embeddings.shape[1]
    index=faiss.IndexFlatL2(dimension)
    embeddings=np.asarray(embeddings,dtype=np.float32)

    index.add(embeddings)
    return index

def search_vectors(index,query_embedding,k=3):
    query_embedding=np.asarray(
        query_embedding,
        dtype=np.float32
    ).reshape(1,-1)

    distances, indices=index.search(query_embedding,k)
    return distances[0], indices[0]