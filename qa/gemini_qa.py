import google.generativeai as genai
import faiss
import numpy as np


def get_gemini_embeddings(text_list):
    embeddings = []
    for text in text_list:
        response = genai.embed_content(
            model="models/embedding-001", content=text, task_type="retrieval_document"
        )
        embeddings.append(response["embedding"])
    return embeddings


def build_faiss_index(embeddings):
    """
    Builds a FAISS index from a list of embedding vectors.

    Args:
        embeddings (List[List[float]]): List of embedding vectors.

    Returns:
        faiss.IndexFlatL2: FAISS index.
    """
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    return index


def get_top_k_chunks(query, index, chunks, k=5):
    """
    Retrieves top-k most relevant chunks for the query from the FAISS index.

    Args:
        query (str): User's question.
        index (faiss.IndexFlatL2): FAISS index.
        chunks (List[str]): Original text chunks.
        k (int): Number of top results to return.

    Returns:
        List[str]: Top-k relevant chunks.
    """
    query_embedding = genai.embed_content(
        model="models/embedding-001", content=query, task_type="retrieval_query"
    )["embedding"]
    D, I = index.search(np.array([query_embedding]).astype("float32"), k)
    return [chunks[i] for i in I[0]]


def generate_answer(question, context_chunks):
    """
    Generates an answer to a user question based on provided context.

    Args:
        question (str): The user's input question.
        context_chunks (List[str]): Relevant chunks from the document.

    Returns:
        str: The generated answer.
    """
    # Combine context chunks into a single string
    context = "\n".join(context_chunks)
    # Create prompt for the language model
    prompt = f"""You are an AI assistant. Use the following context to answer the user's query.

Context:
{context}

Question: {question}
Answer:"""

    model = genai.GenerativeModel("models/gemini-1.5-flash")  # Load Gemini model

    # Generate answer from the model
    response = model.generate_content(prompt)
    return response.text


# def gemini_qa_flow_from_memory(question):
#     top_chunks = get_top_k_chunks(
#         question,
#         st.session_state.gemini_index,
#         st.session_state.chunks
#     )
#     return generate_answer(question, top_chunks)
