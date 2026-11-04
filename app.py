"""HTTP API for the LegalLens React application."""

from __future__ import annotations

import os
import tempfile
import uuid
from pathlib import Path
from threading import Lock

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="LegalLens API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)

_sessions: dict[str, dict] = {}
_sessions_lock = Lock()
_MAX_UPLOAD_BYTES = 25 * 1024 * 1024


def _get_pipeline():
    """Load the embedding model only when a document is first processed."""
    from src.rag_pipeline import build_rag_index, generate_answer, retrieve_context

    return build_rag_index, generate_answer, retrieve_context


class Question(BaseModel):
    question: str


def _index_pdf(path: str, filename: str) -> dict:
    try:
        build_rag_index, _, _ = _get_pipeline()
        index, chunks = build_rag_index(path)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Could not process this PDF: {exc}") from exc
    if not chunks:
        raise HTTPException(status_code=422, detail="No readable text was found in this PDF.")
    session_id = str(uuid.uuid4())
    with _sessions_lock:
        _sessions[session_id] = {"index": index, "chunks": chunks}
    return {
        "session_id": session_id,
        "filename": filename,
        "pages": len({chunk["page_number"] for chunk in chunks}),
        "chunks": len(chunks),
        "message": "Your document is ready for questions.",
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "LegalLens API"}


@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)):
    filename = Path(file.filename or "document.pdf").name
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Please choose a PDF document.")
    contents = await file.read(_MAX_UPLOAD_BYTES + 1)
    if len(contents) > _MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="PDFs must be smaller than 25 MB.")
    if not contents.startswith(b"%PDF"):
        raise HTTPException(status_code=415, detail="This file does not appear to be a valid PDF.")
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name
        return _index_pdf(temp_path, filename)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/api/demo")
def load_demo_document():
    demo_path = Path(__file__).parent / "data" / "documents" / "employee-agreement.pdf"
    if not demo_path.exists():
        raise HTTPException(status_code=404, detail="The sample agreement is not available.")
    return _index_pdf(str(demo_path), demo_path.name)


@app.post("/api/sessions/{session_id}/questions")
def ask_question(session_id: str, payload: Question):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Enter a question about your document.")
    with _sessions_lock:
        session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="This document session has expired. Upload it again.")
    try:
        _, generate_answer, retrieve_context = _get_pipeline()
        sources = retrieve_context(question, session["index"], session["chunks"])
        answer = generate_answer(question, sources) if sources else "I couldn't find relevant information in this document."
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Answer generation failed: {exc}") from exc
    return {"answer": answer, "sources": sources}


@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    with _sessions_lock:
        _sessions.pop(session_id, None)
    return {"status": "cleared"}
