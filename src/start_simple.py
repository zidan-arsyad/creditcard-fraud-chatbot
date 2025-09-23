import streamlit as st
from time import sleep

st.set_page_config(
    page_title="Credit Fraud Assistant", page_icon="💳", layout="centered"
)
st.title("Chat with Credit Fraud Analyst AI")

# Check agents
if "is_initialized" not in st.session_state:
    st.session_state.is_initialized = False
    st.session_state.main_agent = None
    st.session_state.chat_history = []

@st.cache_resource(show_spinner=False)
def init_agents():
    from scripts.agents.main_agent import MainAgent

    with st.spinner("Calling agent..."):
        main_agent = MainAgent(memory_limit=50).create_main_agent()

    st.session_state.main_agent = main_agent
    st.session_state.is_initialized = True


if not st.session_state.is_initialized:
    init_agents()

def print_chat_history():
    """Render all messages except the very last assistant message (to avoid duplicate after streaming)."""
    for message in st.session_state.chat_history:
        if message["role"] in ["user", "assistant"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

def stream_message(text):
    """Stream assistant text word by word."""
    placeholder = st.empty()
    streamed_text = ""
    for word in text:
        streamed_text += word
        placeholder.markdown(streamed_text)
        sleep(0.02)
    return placeholder


if st.session_state.is_initialized:
    # Initialize processing flag if not exists
    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False
    
    # Display existing chat history
    print_chat_history()
    
    # Get user input
    user_input = st.chat_input("Ask me anything about credit card fraud!", disabled=st.session_state.is_processing)
    if user_input and not st.session_state.is_processing:
        # Set processing flag
        st.session_state.is_processing = True
        
        # Add and display user message
        user_message = {"role": "user", "content": user_input}
        st.session_state.chat_history.append(user_message)
        
        # Display the user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Process and stream assistant response
        main_agent = st.session_state.main_agent
        config = {"configurable": {"thread_id": "1"}}

        try:
            # Create assistant message container
            with st.chat_message("assistant"):
                with st.spinner("Formulating answer..."):
                    response = main_agent.invoke(
                        {"messages": user_message}, 
                        config=config
                    )
                    final_output = response["messages"][-1].content
                
                # Stream the response
                stream_message(final_output)
            
            # Add assistant response to history
            st.session_state.chat_history.append({
                "role": "assistant", 
                "content": final_output
            })
            
            print(f"Final output: {final_output}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Reset processing flag
            st.session_state.is_processing = False
            st.rerun()