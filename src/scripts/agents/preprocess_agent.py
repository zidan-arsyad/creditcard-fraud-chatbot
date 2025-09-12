from langchain.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from scripts.inputs import (
    REWRITE_INPUT_PROMPT,
    FILTER_INPUT_PROMPT,
)


class PreprocessAgent:
    def __init__(self, llm, history):
        self.llm = llm
        self.history = history

    def _rewrite_input_chain(self):
        """Rewrite the original user input"""

        rewrite_input_prompt = PromptTemplate(
            input_variables=["user_input", "history"],
            template=REWRITE_INPUT_PROMPT,
        )

        rewrite_chain = (
            RunnableParallel(
                user_input=RunnablePassthrough(), history=RunnablePassthrough()
            )
            | rewrite_input_prompt
            | self.llm
            | {"list_requests": RunnablePassthrough()}
        )

        # print("Rewrite Chain:", type(rewrite_chain))
        return rewrite_chain

    def _rewrite_printer(self, x):
        print(f"Rewrited request: {x['list_requests'].content}")
        return x

    def _filter_input_chain(self):
        """Filter out off-topic user requests"""

        filter_input_prompt = PromptTemplate(
            input_variables=["list_requests"],
            template=FILTER_INPUT_PROMPT,
        )

        filter_chain = (
            {"list_requests": RunnablePassthrough()}
            | filter_input_prompt
            | self.llm
            | {"filtered_requests": RunnablePassthrough()}
        )

        # print("Filter Chain:", type(filter_chain))
        return filter_chain

    def preprocess_request(self, user_input: str) -> str:
        """Get the filtered list of user requests from user input"""

        rewrite_chain = self._rewrite_input_chain()
        filter_chain = self._filter_input_chain()

        rewrite_printer_runnable = RunnableLambda(self._rewrite_printer)

        # Compose the chains
        preprocess_chain = rewrite_chain | rewrite_printer_runnable | filter_chain

        filtered_requests = preprocess_chain.invoke(
            {"user_input": user_input, "history": self.history}
        )["filtered_requests"]

        # print("Filtered Requests:", filtered_requests.content)
        return filtered_requests

    def set_history(self, history):
        self.history = history
