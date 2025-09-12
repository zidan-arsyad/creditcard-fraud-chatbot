import sys
sys.path.insert(1, "D:\Projects\creditcard-fraud-chat")

from langchain.tools.retriever import create_retriever_tool
from scripts.utils.vector_stores import get_vector_stores
from scripts.inputs.prompts import DOCUMENTS_QUERY_AGENT_PROMPT


def get_doc_tool(top_k=5):
    doc_vector_store = get_vector_stores()
    doc_retriever = doc_vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": top_k}
    )

    doc_tool = create_retriever_tool(
        retriever=doc_retriever,
        name="doc_tool",
        description="Tool for accessing stored document as reference to answer questions about credit card frauds",
    )
    return doc_tool

def get_doc_prompt(top_k=5):
    doc_prompt = DOCUMENTS_QUERY_AGENT_PROMPT.format(top_k=top_k)
    return doc_prompt
