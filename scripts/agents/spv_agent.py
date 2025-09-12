import sys
sys.path.insert(1, "D:\Projects\creditcard-fraud-chat")

from langgraph_supervisor import create_supervisor
from scripts.inputs.prompts import SUPERVISOR_AGENT_PROMPT

from scripts.agents.sql_agent import SqlAgent
from scripts.agents.doc_agent import DocAgent


class SpvAgent:
    def __init__(self, llm):
        self.llm = llm
        self.sql_agent = SqlAgent(llm=self.llm).create_sql_agent()
        self.doc_agent = DocAgent(llm=self.llm).create_doc_agent()

    def create_spv_agent(self):
        spv_agent = create_supervisor(
            model=self.llm,
            agents=[self.sql_agent, self.doc_agent],
            parallel_tool_calls=True,
            prompt=SUPERVISOR_AGENT_PROMPT,
            name="spv_agent",
            output_mode="last_message",
            timeout=15,
            max_iterations=5
        )
        return spv_agent.compile()
