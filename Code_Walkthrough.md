# Code Walkthrough: Excel QA Agent

## 1. Streamlit UI (`main.py`)

- Handles file upload via `st.file_uploader`. 
- Provides radio option between single and multiple document uploads
- Provides radio options to choose between Direct Gemini and LangChain mode.
- Invokes respective QA flows (`gemini_qa_flow` or `langchain_qa_flow`).
- Displays the final answer to the user.

## 2. Excel Parsing (`file_parser.py`)
```python
def parse_excel(file_path: str) -> List[str]:
    # Converts each row of Excel to natural language format
    # Example: Row 1: "Column A is X, Column B is Y"
```
- Supports `.xlsx`, `.xls`, and `.csv` formats.
- Ensures each row is converted into a meaningful sentence.

## 3. Direct Gemini QA (`gemini_qa.py`)

### Embedding
```python
def get_gemini_embeddings(text_list):
    # Uses Google Gemini's "models/embedding-001" for document embeddings.
```
### Indexing
```python
def build_faiss_index(embeddings):
    # Creates an in-memory FAISS vector index from embeddings.
```
### Retrieval + LLM
```python
def generate_answer(question, context_chunks):
    # Combines the retrieved context chunks into a prompt.
    # Uses Gemini to generate an answer.
```

## 4. LangChain Flow (`langchain_qa.py`)

- Uses LangChain’s `GoogleGenerativeAIEmbeddings` and `ChatGoogleGenerativeAI` classes.
- Wraps LLM and Retriever with `RetrievalQA` Chain.
- Automatically handles chunk retrieval and prompt formatting.

## 5. Key Design Decisions

- **Row-Level Sentences**: Ensures better semantic parsing compared to columnar tokenization.
- **FAISS**: Chosen for fast and scalable vector search.
- **Modular Structure**: Clear separation between UI, utilities, and LLM flows.

## 6. Challenges Addressed

- **Chunking Strategy**: Initially tried naive chunking, then shifted to row-based natural language.
- **API Limits**: Handled Gemini's content embedding and generation quota efficiently.
- **LangChain Compatibility**: Ensured seamless compatibility by modularizing dependencies.
- **API Availability**: I only have gemini key avaialbel with me, so I have used this.

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