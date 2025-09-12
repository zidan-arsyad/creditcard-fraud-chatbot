from langgraph.prebuilt import create_react_agent
from scripts.tools.doc_tool import get_doc_tool, get_doc_prompt


class DocAgent:
    def __init__(self, llm, top_k=5):
        self.llm = llm
        self.top_k = top_k

    def create_doc_agent(self):
        doc_tool = get_doc_tool()

        doc_agent = create_react_agent(
            model=self.llm,
            tools=[doc_tool],
            prompt=get_doc_prompt(),
            name="doc_agent",
        )
        return doc_agent