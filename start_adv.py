from dotenv import load_dotenv

import streamlit as st
from time import sleep

from scripts.agents import spv_agent
from scripts.utils.llm import LLM
from scripts.agents.preprocess_agent import PreprocessAgent
from scripts.agents.spv_agent import SpvAgent

from langchain_core.messages import HumanMessage

load_dotenv()

st.set_page_config(
    page_title="Credit Fraud Assistant", page_icon="💳", layout="centered"
)
st.title("Chat with Credit Fraud Anaylst Chatbot")


@st.cache_resource
def init_agents():
    llm = LLM().get_llm()
    prep_agent = PreprocessAgent(llm=llm, history=None)
    spv_agent = SpvAgent(llm=llm).create_spv_agent()
    return (llm, prep_agent, spv_agent)


with st.spinner("Loading agent..."):
    (st.session_state.llm, st.session_state.prep_agent, st.session_state.spv_agent) = (
        init_agents()
    )

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


def print_chat(message):
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# print messages from chat history
for message in st.session_state.messages:
    print_chat(message)


def stream_message(message_stream):
    for word in message_stream:
        yield word
        sleep(0.02)


user_input = st.chat_input("Ask me anything about credit card fraud detection!")
if user_input:
    llm = st.session_state.llm
    prep_agent = st.session_state.prep_agent
    spv_agent = st.session_state.spv_agent

    message_input = {"role": "user", "content": user_input}
    st.session_state.messages.append(message_input)
    history = st.session_state.messages
    prep_agent.set_history(history)

    # print current user input to chat
    print_chat(message_input)

    # preprocess user input
    preprocessed_request = prep_agent.preprocess_request(user_input=user_input)
    clean_request = preprocessed_request.content
    print(f"Clean request: {clean_request}")

    try:
        with st.chat_message("assistant"):
            with st.spinner("Formulating answer..."):
                response = spv_agent.invoke(
                    {"messages": [HumanMessage(content=clean_request)]}
                )
                final_output = response["messages"][-1].content

            st.write_stream(stream_message(final_output))
            print(f"Final output: {final_output}")
        st.session_state.messages.append({"role": "assistant", "content": final_output})
    except Exception as e:
        st.error(e)
