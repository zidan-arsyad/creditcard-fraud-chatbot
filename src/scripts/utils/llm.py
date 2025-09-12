from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


class LLM:
    """Initialize and provide access to the language model."""

    def __init__(self):
        load_dotenv()

        self.llm = init_chat_model(
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            model_provider="groq",
            temperature=0.0,
            max_retries=3,
            timeout=10,
        )

    def get_llm(self):
        return self.llm
