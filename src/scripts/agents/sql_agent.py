from langgraph.prebuilt import create_react_agent
from scripts.tools.sql_tool import get_sql_tool, get_sql_prompt


class SqlAgent:
    def __init__(self, llm):
        self.llm = llm

    def create_sql_agent(self):
        sql_tool = get_sql_tool(llm=self.llm)

        sql_agent = create_react_agent(
            model=self.llm,
            tools=sql_tool,
            prompt=get_sql_prompt(),
            name="sql_agent",
        )
        return sql_agent
