import sys

sys.path.insert(1, "D:\Projects\creditcard-fraud-chat")

from langgraph.prebuilt import create_react_agent
from langchain.memory import ConversationBufferWindowMemory
from scripts.inputs.prompts_main import MAIN_AGENT_PROMPT
from scripts.tools.sql_tool import get_sql_tool
from scripts.tools.doc_tool import get_doc_tool


class MainAgent:
    def __init__(self, llm, limit_memory=10):
        self.llm = llm
        self.memory = ConversationBufferWindowMemory(
            memory_key="history",
            k=limit_memory,
            return_messages=True,
        )

    def create_main_agent(self):
        doc_tool = get_doc_tool()
        sql_tool = get_sql_tool(llm=self.llm)  # returns a list

        main_agent = create_react_agent(
            self.llm,
            tools=sql_tool + [doc_tool],
            memory=self.memory,
            prompt=MAIN_AGENT_PROMPT,
        )
        return main_agent