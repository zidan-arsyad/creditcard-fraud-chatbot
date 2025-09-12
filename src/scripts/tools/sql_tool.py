from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from scripts.utils.db import get_db
from scripts.inputs import SQL_TOOL_PROMPT


def get_sql_tool(llm):
    db = get_db()
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    sql_tool = sql_toolkit.get_tools()[0]
    sql_tool.name = "sql_tool"
    sql_tool.description = "Tool for accessing credit card users and frauds data."
    return sql_toolkit.get_tools()


def get_sql_prompt(dialect="sqlite", top_k=5):
    sql_prompt = SQL_TOOL_PROMPT.format(dialect=dialect, top_k=top_k)
    return sql_prompt
