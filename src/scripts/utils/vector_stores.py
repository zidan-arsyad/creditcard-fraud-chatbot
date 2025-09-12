import os
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pymupdf4llm import PyMuPDF4LLMParser

import faiss
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.docstore import InMemoryDocstore
from langchain_core.vectorstores import InMemoryVectorStore


def _parse_document(file_path):
    """Parse a document file into pages."""

    loader = GenericLoader(
        blob_loader=FileSystemBlobLoader(path=file_path),
        blob_parser=PyMuPDF4LLMParser(
            mode="page",
        ),
    )
    pages = []
    for doc in loader.lazy_load():
        pages.append(doc)
    return pages


def _get_documents_from_folder(folder_path, file_type):
    """Load all PDF documents from a folder and parse them into pages."""

    documents_list = os.listdir(folder_path)
    print(f"Found {len(documents_list)} documents in folder {folder_path}")

    documents = []
    for filename in documents_list:
        if filename.endswith(file_type):
            file_path = os.path.join(folder_path, filename)
            document = _parse_document(file_path)
            documents.extend(document)
    print(f"Total document pages loaded: {len(documents)}")  # Number of pages parsed
    return documents


def _split_documents(documents):
    """Split documents into smaller chunks for better retrieval performance."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # chunk size (characters)
        chunk_overlap=200,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )
    docs_splits = text_splitter.split_documents(documents)

    print(f"Total document splits: {len(docs_splits)}")  # Number of chunks created
    return docs_splits


def _create_vector_stores(documents):
    """Create a vector store from documents for semantic search."""

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    index = faiss.IndexFlatL2(len(embedding.embed_query("mekari technical test")))

    vector_store = FAISS(
        embedding_function=embedding,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    documents_splitted = _split_documents(documents)

    vector_store = InMemoryVectorStore(embedding=embedding)
    _ = vector_store.add_documents(documents_splitted)

    print(f"Created vector store: {vector_store}")
    return vector_store


def _documents_ingest(folder_path="data/documents", file_type=".pdf"):
    """Ingest PDF documents from a folder and create a vector store."""

    folder_path = folder_path
    documents = _get_documents_from_folder(folder_path, file_type)
    vector_store = _create_vector_stores(documents)
    return vector_store


def get_vector_stores(replace=False, folder_path="data/processed", file_type=".pdf"):
    """Get or create a vector store, optionally replacing the existing one."""

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    vector_store = InMemoryVectorStore(embedding=embedding)

    file_path = f"{folder_path}/{file_type.split('.')[1]}DocsVector"
    isVectorExists = os.path.exists(file_path)

    # If replace is True or vector store file does not exist, create a new vector store
    # Otherwise, load the existing vector store from disk
    if replace or not isVectorExists:
        vector_store = _documents_ingest(folder_path=folder_path, file_type=file_type)
        print(f"New vector type: {type(vector_store)}")
        vector_store.dump(file_path)
        print(f"Saved vector store to disk at {file_path}")
    else:
        vector_store = vector_store.load(
            file_path,
            embedding=embedding,
        )
        print(f"Loaded vector store from disk at {file_path}")
    return vector_store
