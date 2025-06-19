# Comprehensive Documentation: Excel QA Agent

## Overview

This project is an AI-powered Question Answering (QA) system built to analyze Excel documents using Google Gemini, either directly via API or through LangChain integration. The app is accessible via a Streamlit web interface.

The Excel QA Agent is an AI-powered system that allows users to:
* Upload one or more Excel/CSV files.
* Ask natural language questions.
* Get contextually accurate answers from the document data.

It uses:
* Google Gemini for embedding and language generation.
* LangChain (optional) for modular retrieval-based QA.
* Streamlit for a simple, user-friendly UI.
* FAISS for efficient semantic search on embedded data.

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/bharti085/QA_Bot_Gemini.git
cd QA_Bot_Gemini
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Google Gemini API Key
Create a file called config.py:
```bash
GEMINI_API_KEY = "your_google_gemini_api_key"
```

Or Create a `.env` file or export it directly:
```bash
export GEMINI_API_KEY="your_google_gemini_api_key"
```

### 4. Run the Streamlit App
```bash
streamlit run main.py
```

---

## System Architecture

```text
    ┌─────────────────────┐
    │    Streamlit UI     │ ◄── User uploads, chooses mode, and asks questions
    └────────┬────────────┘
             ▼
  ┌────────────────────────────┐
  │  File Parser & Preprocessor│ ◄── Each row → sentence + tags
  └────────┬───────────────────┘
           ▼
    ┌───────────────┬────────────────────┐
    │ Gemini Flow   │  LangChain Flow    │ ◄── Parallel flows based on  QA mode
    └────┬──────────┴────────────┬───────┘
         ▼                       ▼
   Embedding + FAISS       LangChain Vectorstore
         ▼                       ▼
     Top-k Retrieval       RetrievalQA Chain
         ▼                       ▼
    Gemini LLM QA          Gemini LLM via Chain
         ▼                       ▼
         └────→ Answer returned to UI
```
---

## Components Description

---

### `main.py`
- Handles file upload (single/multiple).
- Mode selection between **Direct Gemini** and **LangChain**.
- Manages session state for:
  - Embedding reuse  
  - QA mode switching  
- Displays the final answer in the Streamlit UI.

---

### `utils/file_parser.py`
- Converts each row of Excel/CSV to a natural sentence like:  
  `"Row 2: Product is Fevicol, Sales is 5000, Region is North"`
- Tags each row with row number (and optionally file name).
- Supports **mixed-schema files** during multi-upload.

---

### `qa/gemini_qa.py`
- Embeds document chunks using Gemini’s `embedding-001`.
- Builds a **FAISS index** for semantic similarity search.
- Retrieves top-k similar rows to the user query.
- Uses `gemini-1.5-flash` to generate the final answer.

---

### `qa/langchain_qa.py`
- Uses `GoogleGenerativeAIEmbeddings` for vector generation.
- Uses `ChatGoogleGenerativeAI` as the LLM.
- Wraps embedding + LLM inside a LangChain `RetrievalQA` chain.

---

### `config.py`
- Stores your **Google Gemini API key** securely.

---

## Feature Highlights

- Upload multiple files (`.xlsx`, `.xls`, `.csv`) at once.
- Ask **unlimited questions** without needing to re-upload files.
- Automatically recomputes embeddings only if:
  - A new file is uploaded  
  - QA mode is changed  
- Choose between:
  - **Gemini (Direct)** → Fast & simple
  - **Gemini via LangChain** → Modular & scalable
- Uses **FAISS + Gemini embeddings** for accurate document retrieval.
- Supports **tagged source tracking** for multi-file QA  
  _e.g._ `[Source: sales.xlsx] Row 3: Product is Fevicol...`

---

## Session State Tracking

| Variable           | Description                                        |
|--------------------|----------------------------------------------------|
| `file_fingerprint` | Stores hash of uploaded filenames                  |
| `active_qa_mode`   | Tracks the currently selected QA mode              |
| `chunks`           | Stores parsed row-level text from documents        |
| `gemini_index`     | FAISS index created using Gemini embeddings        |
| `qa_chain`         | LangChain `RetrievalQA` chain for LangChain mode   |

---

## Known Limitations

- Only supports `.xlsx`, `.xls`, and `.csv` files.
- PDF, DOCX, and images are not supported yet.
- No persistent vector DB — FAISS is in-memory only.
- Only Gemini is integrated (no OpenAI, Claude, etc.).
- Streamlit session resets if page is refreshed.

---

## Future Scope

### Model Flexibility
- Add support for OpenAI, Claude, LLaMA, Mistral, etc.
- Allow dynamic model switching from the UI.

### Transformer-Based Local QA
- Integrate Hugging Face `sentence-transformers` for local embeddings.
- Ideal for on-premise / air-gapped environments.

### Persistent Vector Store
- Use ChromaDB, Redis, or Pinecone for long-term embedding storage.

### Document Type Expansion
- Add support for PDF, DOCX, and even scanned/image tables.

### Session Memory & Feedback
- Enable persistent chat memory via LangChain.
- Improve user feedback loop and traceability.

### Explainability & Source Tracing
- Highlight which rows or files contributed to the final answer.
