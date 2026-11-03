import os 

from dotenv import load_dotenv
from groq import Groq

from src.ingestion import extract_pdf
from src.chunking import create_chunks
from src.embeddings import model, generate_embeddings

from src.vector_store import(
    create_vector_store,
    search_vectors
)

load_dotenv()

client=Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def build_rag_index(pdf_path):
    pages = extract_pdf(pdf_path)

    chunks = create_chunks(pages)

    embeddings = generate_embeddings(chunks)

    index = create_vector_store(embeddings)

    return index, chunks

def retrieve_context(query,index,chunks,k=3):
    query_embedding=model.encode([query])

    distances,indices=search_vectors(
        index,
        query_embedding,
        k

    )

    retrieved_chunks=[]

    for idx in indices:
        if idx==-1:
            continue

        retrieved_chunks.append(chunks[idx])
    return retrieved_chunks

def generate_answer(query,retrieved_chunks):

    context="\n\n".join(
        [
            f"Page {chunk["page_number"]}: {chunk["text"]}"
            for chunk in retrieved_chunks
        ]
    )
    prompt= f"""
    You are a helpful legal document assistant.

    Answer the question using ONLY the provided document context.

    Rules:
    1. Do not invent information.
    2. If the answer is not in the context, say so.
    3. Cite the page number supporting your answer.
    4. Keep the answer simple and clear.

    DOCUMENT CONTEXT:
    {context}

    QUESTION:
    {query}

    ANSWER:
    """

    response=client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.1
    )

    return response.choices[0].message.content

if __name__ == "__main__":

    pdf_path = "data/documents/employee-agreement.pdf"

    index, chunks = build_rag_index(pdf_path)

    print("Legal RAG system ready!")

    while True:
        query = input("\nAsk a question (type exit to quit): ")

        if query.lower() == "exit":
            break

        retrieved_chunks = retrieve_context(
            query,
            index,
            chunks
        )

        answer = generate_answer(
            query,
            retrieved_chunks
        )

        print("\nAnswer:")
        print(answer)
