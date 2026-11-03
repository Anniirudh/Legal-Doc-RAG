from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.ingestion import extract_pdf

def create_chunks(pages,chunk_size=500,chunk_overlap=100):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n","\n",". "," ",""]
    )

    chunks=[]

    for page in pages:
        page_chunks=splitter.split_text(page["text"])
        for index,chunk in enumerate(page_chunks):
            chunks.append({
                "chunk_id":len(chunks),
                "page_number":page["page_number"],
                "text":chunk
            })

    return chunks

if __name__ == "__main__":
    pages=extract_pdf(
        "data/documents/employee-agreement.pdf"
    )
    chunks=create_chunks(pages)

    print(f"Total chunks: {len(chunks)}")

    for chunk in chunks[:5]:
        print("\n---------------")
        print(f"Chunk ID: {chunk["chunk_id"]}")
        print(f"Page: {chunk["page_number"]}")
        print(chunk["text"])