
import streamlit as st
import tempfile
import os

from src.rag_pipeline import (
    build_rag_index,
    retrieve_context,
    generate_answer
)


st.set_page_config(
    page_title="LegalLens AI",
    page_icon="📄",
    layout="wide"
)


st.title("📄 LegalLens AI")
st.caption("Ask questions about your legal documents using RAG.")

# Session state
if "index" not in st.session_state:
    st.session_state.index = None

if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:

    st.header("Upload Document")

    uploaded_file = st.file_uploader(
        "Upload an employment agreement",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button("Process Document"):

            with st.spinner("Processing PDF..."):

                temp_path = None

                try:
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as temp_file:

                        temp_file.write(uploaded_file.getvalue())
                        temp_path = temp_file.name

                    index, chunks = build_rag_index(temp_path)

                    st.session_state.index = index
                    st.session_state.chunks = chunks
                    st.session_state.messages = []

                    st.success("Document processed successfully!")

                except Exception as e:
                    st.error(f"Processing failed: {e}")

                finally:
                    if temp_path and os.path.exists(temp_path):
                        os.remove(temp_path)


# Main interface
if st.session_state.index is None:

    st.info("Upload and process a PDF to start asking questions.")

else:

    st.success("Document ready for questions!")

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if "sources" in message:
                with st.expander("View retrieved sources"):
                    for source in message["sources"]:
                        st.write(
                            f"Page {source['page_number']}:"
                        )
                        st.write(source["text"])

    # User input
    query = st.chat_input("Ask something about your document...")

    if query:

        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):

            with st.spinner("Searching document..."):

                retrieved_chunks = retrieve_context(
                    query,
                    st.session_state.index,
                    st.session_state.chunks
                )

                if not retrieved_chunks:
                    answer = "I couldn't find relevant information in the document."
                else:
                    answer = generate_answer(
                        query,
                        retrieved_chunks
                    )

                st.markdown(answer)

                with st.expander("View retrieved sources"):
                    for source in retrieved_chunks:
                        st.write(
                            f"Page {source['page_number']}:"
                        )
                        st.write(source["text"])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": retrieved_chunks
                })
