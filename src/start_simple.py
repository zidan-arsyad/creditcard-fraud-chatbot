import streamlit as st
from time import sleep

from scripts.utils.llm import LLM
from scripts.agents.main_agent import MainAgent


st.set_page_config(
    page_title="Credit Fraud Assistant", page_icon="💳", layout="centered"
)
st.title("Chat with Credit Fraud Analyst AI")


@st.cache_resource
def init_agents():
    llm = LLM().get_llm()
    main_agent = MainAgent(llm=llm).create_main_agent()
    return (llm, main_agent)


def print_chat(message):
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def stream_message(message_stream):
    for word in message_stream:
        yield word
        sleep(0.02)


with st.spinner("Loading agent..."):
    (st.session_state.llm, st.session_state.main_agent) = init_agents()

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# print messages
for message in st.session_state.messages:
    print_chat(message)

user_input = st.chat_input("Ask me anything about credit card fraud!")
if user_input:
    llm = st.session_state.llm
    main_agent = st.session_state.main_agent

    message_input = {"role": "user", "content": user_input}
    st.session_state.messages.append(message_input)
    print_chat(message_input)

    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            streamed_text = ""

            with st.spinner("Formulating answer..."):
                response = main_agent.invoke({"messages": [message_input]})
                final_output = response["messages"][-1].content

            print(f"Response type: {type(response)}")
            print(f"Final output type: {type(final_output)}")
            print(f"Final output: {final_output}")

            # stream the output word by word
            for word in final_output:
                streamed_text += word
                response_placeholder.markdown(streamed_text)
                sleep(0.02)

        st.session_state.messages.append({"role": "assistant", "content": final_output})

        main_agent.memory.chat_memory.add_user_message(user_input)
        main_agent.memory.chat_memory.add_ai_message(final_output)

    except Exception as e:
        st.error(e)
