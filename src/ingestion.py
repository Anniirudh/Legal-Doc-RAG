import pymupdf
from pathlib import Path

def extract_pdf(pdf_path:str):
    """
    Extract text from a PDF while preserving page numbers.

    Returns:
        List of dictionaries containing page number and text.
    """

    documents=[]
    pdf_path=Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    with pymupdf.open(pdf_path) as pdf:
        for page_number,page in enumerate(pdf,start=1):
            text=page.get_text("text").strip()
            if text:
                documents.append({
                    "page_number":page_number,
                    "text":text.strip()
                })
    return documents

if __name__=="__main__":
    pdf_path="data/documents/employee-agreement.pdf"
    pages=extract_pdf(pdf_path)
    print(f"Total pages extracted: {len(pages)}")
    for page in pages:
        print(f"\n--- Page {page['page_number']} ---")
        print(page['text'][:500])