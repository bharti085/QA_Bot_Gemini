import os
import pandas as pd
from typing import List
from langchain.schema import Document


def parse_excel_to_text(file_path: str) -> List[str]:
    """
    Reads an Excel or CSV file and converts each row into a natural language sentence.
    Supports .xlsx, .xls, and .csv formats.

    Args:
        file_path (str): Path to the Excel or CSV file.

    Returns:
        List[str]: List of natural language sentences created from each row.
    """
    print(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")

    all_sentences = []
    extension = os.path.splitext(file_path)[-1].lower()

    try:
        if extension in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
            print(df.head())
        elif extension == ".csv":
            df = pd.read_csv(file_path)
        else:
            raise ValueError("Unsupported file format. Use .xlsx, .xls, or .csv")

        df = df.dropna(how="all")  # Remove completely empty rows
        df = df.fillna("")  # Fill remaining NaNs with empty string

        for idx, row in df.iterrows():
            sentence_parts = [
                f"{col} is {val}" for col, val in row.items() if str(val).strip()
            ]
            sentence = f"Row {idx + 1}: " + ", ".join(sentence_parts)
            all_sentences.append(sentence)

    except Exception as e:
        print(f"Error while processing the file: {e}")
        raise

    return all_sentences


def load_excel_as_documents(file_path):
    """
    Converts each row of an Excel file into a sentence-based Document.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        List[Document]: List of LangChain Documents.
    """
    extension = file_path.split(".")[-1].lower()

    # Load based on file type
    if extension in ["xlsx", "xls"]:
        df = pd.read_excel(file_path)
    elif extension == "csv":
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Use .xlsx, .xls, or .csv")

    df = df.dropna(how="all")  # Remove completely empty rows

    documents = []
    for idx, row in df.iterrows():
        sentence_parts = [
            f"{col} is {val}"
            for col, val in row.items()
            if pd.notnull(val) and str(val).strip()
        ]
        sentence = f"Row {idx + 1}: " + ", ".join(sentence_parts)
        documents.append(Document(page_content=sentence))

    return documents