from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

def build_faiss_vectorstore(documents):
    """
    Builds a FAISS index from a list of embedding vectors.

    Args:
        embeddings (List[List[float]]): List of embedding vectors.

    Returns:
        faiss.IndexFlatL2: FAISS index.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(documents, embedding=embeddings)
    return vectorstore

def build_qa_chain(vectorstore):
    """
    Builds a RetrievalQA chain using LLaMA (or Gemini) LLM and a FAISS vectorstore retriever.

    Args:
        vectorstore (FAISS): Vectorstore built from embedded documents.

    Returns:
        RetrievalQA: LangChain RetrievalQA object ready for question-answering.
    """
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", temperature=0.1)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=True
    )
    return qa_chain