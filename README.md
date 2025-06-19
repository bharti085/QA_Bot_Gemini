
# Excel QA Agent — Gemini & LangChain

An intelligent **AI-powered Question Answering (QA) tool** built with **Google Gemini** and optionally **LangChain**.  
It allows you to upload one or more Excel/CSV documents and ask natural language questions — getting answers based on the document content.

---

## Features

- Upload `.xlsx`, `.xls`, or `.csv` files (Single or Multiple).
- Ask **natural language questions** about the uploaded documents.
- Switch between two QA modes:
  - **Gemini (Direct)** — FAISS-based retrieval + Gemini LLM generation
  - **Gemini via LangChain** — LangChain Retriever + LLM
- Smart parsing: converts rows into natural language-like sentences.
- **Efficient and fast vector search** via FAISS.
- Embeddings & FAISS index are cached for fast multi-question querying.
- Seamless mode switching — no re-upload required.
- Keeps track of file provenance per row when multi-file upload is used.

---

## Installation

```bash
git clone https://github.com/bharti085/QA_Bot_Gemini.git
cd QA_Bot_Gemini
pip install -r requirements.txt
```

---

## Set Google Gemini API Key

Create an environment variable in your terminal:

```bash
export GOOGLE_API_KEY="your-api-key"
```

Or store in a python config file:

```
# config.py
GEMINI_API_KEY = "your-gemini-api-key"
```

---

## Run the App

```bash
streamlit run main.py
```

---

## How it Works

1. **File Upload**
   - Upload 1 or more .xlsx / .csv files.
   - You can toggle between Single or Multiple document mode.

2. **Excel File Parsing**
   - Each row is converted into a natural language sentence like:  
     `"Row 2: Name is John, Age is 25, City is New York."`

3. **Vectorization**
   - Rows are embedded using Gemini's embedding model (`embedding-001`).

4. **Indexing**
   - Embeddings are stored in a **FAISS index** for similarity-based search.

5. QA Flow (2 Modes)
  * **Gemini (Direct)** -	Uses Gemini for both retrieval & answering
  * **LangChain** -	Uses LangChain Retriever + Gemini LLM

6. **Retrieval + Answer Generation**
   - Top-k most relevant rows are retrieved.
   - Gemini LLM (`gemini-1.5-flash`) is used to generate the final answer.

---

## QA Modes

| Mode                  | Description |
|----------------------|-------------|
| **Direct Gemini**     | Uses Google Gemini API directly for both retrieval and generation |
| **Gemini via LangChain** | Uses LangChain's Retriever → QA Chain architecture |

---

## Smart Behavior
  - Embeddings are created once per file upload
  - Supports multiple questions without reprocessing
  - Automatically re-indexes only if:
        * File(s) are changed
        * QA mode is switched

## Tech Stack

- [Streamlit](https://streamlit.io/) – UI
- [Google Gemini](https://ai.google.dev/) – LLM + Embeddings
- [LangChain](https://www.langchain.com/) – Optional QA orchestration
- [FAISS](https://github.com/facebookresearch/faiss) – Vector database
- [Pandas](https://pandas.pydata.org/) – Excel processing

---

## Requirements

```
streamlit
pandas
openpyxl
faiss-cpu
google-generativeai
langchain
langchain-community
langchain-google-genai
scikit-learn 
```

---

## Future Scope

This project can be extended and scaled in several meaningful ways:

1. **Model Flexibility**  
   ➤ Easily switch between **Gemini**, **LLaMA**, **Mistral**, **OpenAI**, or any other **LLM provider** (Hugging Face, Cohere, etc.).  
   ➤ Add model selection options dynamically in the UI.

2. **Transformer-based Local QA and Hugging Face Support**  
   ➤ Integrate Hugging Face `transformers` and `sentence-transformers` for local embedding generation and answer generation.  
   ➤ Useful for on-premise or air-gapped environments.

3. **Multi-Document QA Support**  
   ➤ Expand to merge documents and trace answers to original files.
   ➤ Enhance with source highlighting or per-document scoring.

4. **Memory & Caching Support**  
   ➤ Store session state using LangChain Memory, Redis, or Chroma.  
   ➤ Cache embeddings and FAISS indexes to avoid recomputation and enable faster interactions.

