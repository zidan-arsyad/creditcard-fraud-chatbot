import os

# === Base Paths ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "processed")


def _parse_document(file_path):
    """Parse a document file into pages."""
    from langchain_community.document_loaders.generic import GenericLoader
    from langchain_community.document_loaders import FileSystemBlobLoader
    from langchain_pymupdf4llm import PyMuPDF4LLMParser

    loader = GenericLoader(
        blob_loader=FileSystemBlobLoader(path=file_path),
        blob_parser=PyMuPDF4LLMParser(mode="page"),
    )
    return list(loader.lazy_load())


def _get_documents_from_folder(folder_path=None, file_type=".pdf"):
    """Load all documents from a folder and parse them into pages."""

    if folder_path is None:
        folder_path = DATA_DIR

    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        print(f"[INFO] Created missing folder: {folder_path}")
        return []

    all_files = os.listdir(folder_path)
    files = [f for f in all_files if f.lower().endswith(file_type)]

    if not files:
        print(f"[WARNING] No {file_type.upper()} files found in {folder_path}.")
        return []

    documents = []
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        documents.extend(_parse_document(file_path))

    print(f"[INFO] Loaded {len(documents)} pages from {len(files)} files.")
    return documents


def _split_documents(documents):
    """Split documents into smaller chunks for better retrieval performance."""
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    if not documents:
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True,
    )
    splits = text_splitter.split_documents(documents)
    print(f"[INFO] Total splits created: {len(splits)}")
    return splits


def _create_vector_stores(documents):
    """Create a vector store from documents for semantic search."""
    if not documents:
        print("[WARNING] No documents to embed. Returning empty vector store.")

    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.docstore import InMemoryDocstore
    import faiss

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"}
    )
    index = faiss.IndexFlatL2(len(embedding.embed_query("placeholder")))

    vector_store = FAISS(
        embedding_function=embedding,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    splits = _split_documents(documents)
    if splits:
        vector_store.add_documents(splits)

    return vector_store


def _documents_ingest(folder_path=None, file_type=".pdf"):
    """Ingest documents from folder and build vector store."""
    documents = _get_documents_from_folder(folder_path, file_type)
    return _create_vector_stores(documents)


def get_vector_stores(replace=False, folder_path=None, file_type=".pdf"):
    """Get or create a FAISS vector store, optionally replacing existing one."""
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS

    if folder_path is None:
        folder_path = DATA_DIR

    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"}
    )
    vector_store_path = os.path.join(folder_path, f"{file_type.strip('.')}_docs_vector")

    is_vector_exists = os.path.exists(vector_store_path)

    if replace or not is_vector_exists:
        vector_store = _documents_ingest(folder_path=folder_path, file_type=file_type)
        if vector_store:
            vector_store.save_local(vector_store_path)
            print(f"[INFO] Saved FAISS vector store at {vector_store_path}")
        else:
            print("[WARNING] No documents found. Vector store not saved.")
            return None
    else:
        vector_store = FAISS.load_local(
            vector_store_path,
            embeddings=embedding,
            allow_dangerous_deserialization=True,
        )
        print(f"[INFO] Loaded FAISS vector store from {vector_store_path}")

    return vector_store
