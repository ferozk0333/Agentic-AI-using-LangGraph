import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
## message_history = []   # List of dictionaries

config = {'configurable':{'thread_id':'1'}}
#{'role':'user', 'content':'Hello!'}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_message = st.chat_input('Type Here')

if user_message:

    st.session_state['message_history'].append({'role': 'user', 'content':user_message})
    with st.chat_message('user'):
        st.text(user_message)

    # Logic for LLM chat with streaming functionality

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_message)]}, 
                config=config,
                stream_mode='messages'
            )
        )  # Assuming ai_message is a streamable object
   
    # Add message to session_state and print
    st.session_state['message_history'].append({'role': 'assistant', 'content':ai_message})
