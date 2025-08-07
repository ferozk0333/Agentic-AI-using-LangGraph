import streamlit as st
from langgraph_backend import chatbot, llm
from langchain_core.messages import HumanMessage
import uuid

# **************************************** utility functions *************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']

def generate_chat_title():
    if not st.session_state['message_history']:
        prompt = f"Concise and simple. Generate a 3-5 word heading for this conversation based on the following user message: {user_input}"
        title = llm.invoke(prompt)
        st.session_state['chat_title'].append({'thread_id': st.session_state['thread_id'], 'title': title.content})
        return title.content


# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

if 'chat_title' not in st.session_state:
    st.session_state['chat_title'] = []

add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI *********************************

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:

    for item in st.session_state['chat_title']:
        if item['thread_id'] == thread_id:
            if st.sidebar.button(str(item['title'])):
                st.session_state['thread_id'] = thread_id
                messages = load_conversation(thread_id)

                temp_messages = []
                role = ""
                for msg in messages:
                    if isinstance(msg, HumanMessage):
                        role='user'
                    else:
                        role='assistant'
                    temp_messages.append({'role': role, 'content': msg.content})

                st.session_state['message_history'] = temp_messages


# **************************************** Main UI ************************************

# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')
     
if user_input:

    # Generating title
    print(generate_chat_title())

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})