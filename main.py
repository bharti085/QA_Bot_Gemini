import streamlit as st
from qa.gemini_qa import (
    get_gemini_embeddings,
    build_faiss_index,
    get_top_k_chunks,
    generate_answer,
)
from qa.langchain_qa import build_faiss_vectorstore, build_qa_chain
from utils.file_parser import parse_excel_to_text, load_excel_as_documents
import os
import numpy as np
from config import GEMINI_API_KEY
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY


# Generate a fingerprint from uploaded file names
def file_fingerprint(files):
    return "_".join(sorted([f.name for f in files]))


# Streamlit UI logic
def run_ui():
    st.set_page_config(page_title="QA App", layout="wide")
    st.title("Excel QA Agent - Gemini & LangChain")

    # --- UI Options ---
    # Upload mode: Single or Multiple files
    doc_mode = st.radio(
        "Choose Upload Mode:", ["Single Document", "Multiple Documents"]
    )
    # QA mode: Direct Gemini or Gemini via Langchain
    qa_mode = st.radio("Choose QA Mode:", ["Gemini (Direct)", "Gemini via LangChain"])

    if "active_qa_mode" not in st.session_state:
        st.session_state.active_qa_mode = qa_mode

    # Upload files
    uploaded_files = None
    if doc_mode == "Single Document":
        file = st.file_uploader("Upload Excel file", type=["xlsx", "xls", "csv"])
        if file:
            uploaded_files = [file]
    else:
        uploaded_files = st.file_uploader(
            "Upload Excel files",
            type=["xlsx", "xls", "csv"],
            accept_multiple_files=True,
        )

    if uploaded_files:
        fingerprint = file_fingerprint(uploaded_files)

        # If uploaded file is new, reprocess
        if (
            st.session_state.get("file_fingerprint") != fingerprint
            or st.session_state.active_qa_mode != qa_mode
        ):
            print("Reprocessing due to new file or QA mode switch...")
            st.session_state.file_fingerprint = fingerprint
            st.session_state.active_qa_mode = qa_mode
            st.session_state.chunks = []

            # Parse uploaded files into row-wise sentences
            with st.spinner("Parsing uploaded files..."):
                for file in uploaded_files:
                    with open("temp.xlsx", "wb") as f:
                        f.write(file.getbuffer())

                    parsed = parse_excel_to_text("temp.xlsx")
                    print(f"Parsed {len(parsed)} rows from {file.name}")
                    st.session_state.chunks.extend(parsed)

            # GEMINI FLOW
            if qa_mode == "Gemini (Direct)":
                with st.spinner("Creating Index..."):
                    print("Using Gemini direct mode")

                    st.session_state.gemini_embeddings = get_gemini_embeddings(
                        st.session_state.chunks
                    )
                    print("Gemini embeddings created")
                    st.session_state.gemini_index = build_faiss_index(
                        st.session_state.gemini_embeddings
                    )
                    print("Gemini FAISS index created")

            # LANGCHAIN FLOW
            elif qa_mode == "Gemini via LangChain":
                with st.spinner("Creating Index..."):
                    print("Using LangChain mode")
                    all_docs = []
                    for file in uploaded_files:
                        with open("temp.xlsx", "wb") as f:
                            f.write(file.getbuffer())

                        docs = load_excel_as_documents("temp.xlsx")
                        print(
                            f"Loaded {len(docs)} LangChain documents from {file.name}"
                        )
                        all_docs.extend(docs)

                    st.session_state.vectorstore = build_faiss_vectorstore(all_docs)
                    print("LangChain vectorstore built")
                    st.session_state.qa_chain = build_qa_chain(
                        st.session_state.vectorstore
                    )
                    print("LangChain QA chain built")

        # Ask a question after files are processed
        question = st.text_input("Ask your question:")
        if question:
            with st.spinner("Thinking..."):
                if qa_mode == "Gemini (Direct)":
                    top_chunks = get_top_k_chunks(
                        question, st.session_state.gemini_index, st.session_state.chunks
                    )
                    print(f"Top {len(top_chunks)} chunks retrieved for question.")

                    answer = generate_answer(question, top_chunks)
                else:
                    answer = st.session_state.qa_chain.invoke(question)["result"]
                    print("LangChain QA chain invoked.")

            st.success(answer)
            print("SUCCESSFULL EXECUTION!!!")


if __name__ == "__main__":
    run_ui()
