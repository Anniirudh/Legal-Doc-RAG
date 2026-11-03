# LegalLens AI 📄

**An AI-powered Legal Document Analyzer built using Retrieval-Augmented Generation (RAG).**

LegalLens AI is a lightweight document question-answering application that allows users to upload legal documents, such as employment agreements and company policies, and ask questions about their contents.

It uses semantic search to retrieve relevant document passages and a Large Language Model (LLM) to generate answers grounded in the uploaded document.

The project demonstrates the fundamental concepts of Retrieval-Augmented Generation, including document ingestion, text chunking, embeddings, vector search, retrieval, and context-aware generation.

## 🚀 Features

- **PDF Ingestion:** Extract text and page numbers from PDF documents using PyMuPDF.
- **Text Chunking:** Split large documents into smaller, manageable chunks with configurable overlap.
- **Text Embeddings:** Generate semantic embeddings using Sentence Transformers.
- **Vector Search:** Store and search document embeddings using FAISS.
- **Semantic Retrieval:** Retrieve relevant passages based on user queries.
- **AI-powered Answers:** Generate context-aware answers using Groq API.
- **Source References:** Display retrieved passages along with their original page numbers.
- **Interactive Interface:** Upload documents and interact with the RAG pipeline through Streamlit.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| PDF Processing | PyMuPDF |
| Text Splitting | LangChain Text Splitters |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| Numerical Operations | NumPy |
| LLM Provider | Groq API |
| LLM Model | GPT-OSS 20B |
| Frontend | Streamlit |

## 🏗️ Architecture

```text
                 PDF Document
                      |
                      v
               PDF Text Extraction
                   (PyMuPDF)
                      |
                      v
                 Text Chunking
                      |
                      v
              Embedding Generation
             (Sentence Transformers)
                      |
                      v
                FAISS Vector Store
                      |
                      |
User Question --------+
      |
      v
Query Embedding
      |
      v
Similarity Search
      |
      v
Relevant Document Chunks
      |
      v
Context Construction
      |
      v
       Groq LLM
      |
      v
Grounded Answer + Sources
```

## 📂 Project Structure

```text
legal-doc-rag/
│
├── app.py
│
├── src/
│   ├── __init__.py
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── rag_pipeline.py
│
├── data/
│   └── documents/
│       └── employee-agreement.pdf
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/legal-doc-rag.git

cd legal-doc-rag
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Groq API

Get an API key from [Groq Console](https://console.groq.com/keys).

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit your API key to GitHub.

### 5. Add a PDF document

Place your PDF inside:

```text
data/documents/
```

For the terminal-based pipeline, update the PDF path in `src/rag_pipeline.py` if necessary.

### 6. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## 🧠 Core RAG Concepts Implemented

### 1. Document Ingestion
Extracts text from PDF documents while preserving page-level information.

### 2. Text Chunking
Splits extracted text into smaller chunks to improve retrieval efficiency.

### 3. Embeddings
Converts text chunks into numerical vector representations using `all-MiniLM-L6-v2`.

### 4. Vector Storage
Stores document embeddings in a FAISS index.

### 5. Similarity Search
Converts user questions into embeddings and retrieves the most relevant document chunks using vector similarity.

### 6. Retrieval-Augmented Generation
Combines retrieved document context with user queries and sends the augmented prompt to a Groq-hosted LLM.

### 7. Grounded Responses
Instructs the LLM to answer using the retrieved document context and provide source page references.

## 🔍 Example Questions

After uploading an employment agreement, users can ask:

- What is the notice period?
- What is the company's leave policy?
- What happens if an employee resigns early?
- What are the employee's responsibilities?
- What are the termination conditions?

The system also supports questions about information that may not be present in the uploaded document.

## 📚 Learning Objectives

This project was developed to understand the practical implementation of Retrieval-Augmented Generation.

Key learning areas:

- Document preprocessing and ingestion
- Text chunking and overlap
- Semantic embeddings
- Vector databases and similarity search
- Top-K retrieval
- Context augmentation
- LLM integration
- Grounded question answering

## 🔮 Future Improvements

- Hierarchical parent-child chunking.
- Hybrid retrieval using BM25 and dense search.
- Cross-encoder reranking.
- Improved citation verification.
- Support for DOCX documents.
- Multi-document question answering.
- Retrieval and answer-quality evaluation.

## ⚠️ Limitations

- Answer quality depends on document extraction and retrieval quality.
- Scanned PDFs may require OCR.
- Retrieved passages do not guarantee that every generated claim is supported.
- The application is intended for educational and informational purposes, not as a substitute for professional legal advice.

## 👨‍💻 Author

**Anirudh**

AI & Machine Learning Student

Interested in Machine Learning, Generative AI, and Retrieval-Augmented Generation.

---

⭐ If you find this project useful, consider giving the repository a star!