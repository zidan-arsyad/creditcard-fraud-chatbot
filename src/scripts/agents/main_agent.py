from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.messages import (
    BaseMessage,
    SystemMessage, 
    trim_messages,
)

from scripts.utils.llm import LLM
from scripts.inputs.prompts_main import MAIN_AGENT_PROMPT


class MainAgent:
    def __init__(self, memory_limit=99):
        self.llm = LLM().get_llm()
        self.memory=InMemorySaver()
        self.memory_limit = memory_limit

    def _pre_model_hook(self, state) -> list[BaseMessage]:
        """Given the agent state, return a list of messages for the chat model."""

        trimmed_history = trim_messages(
            state["messages"],
            token_counter=len,  # len will count the number of messages rather than tokens
            max_tokens=self.memory_limit,
            strategy="last",
            start_on="human",
            end_on=("human", "tool"),
            include_system=False,
            allow_partial=False,
        )

        final_messages = [SystemMessage(content=MAIN_AGENT_PROMPT)] + trimmed_history

        # Debug logging
        print(f"\n=== Message History (limit: {self.memory_limit}) ===")
        for i, msg in enumerate(final_messages):
            msg_type = type(msg).__name__
            content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            print(f"{i}. {msg_type}: {content}")
        print("=" * 50 + "\n")

        return {"llm_input_messages": final_messages}


    def create_main_agent(self):
        from scripts.tools.sql_tool import get_sql_tool
        from scripts.tools.doc_tool import get_doc_tool

        doc_tool = get_doc_tool()
        sql_tool = get_sql_tool(llm=self.llm)

        main_agent = create_react_agent(
            self.llm,
            tools=sql_tool + [doc_tool],
            pre_model_hook=self._pre_model_hook,
            checkpointer=self.memory
        )

        return main_agent
