from langgraph.graph import START, END, StateGraph
from typing import TypedDict, Annotated, List
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
import os

load_dotenv()
OPEN_AI = os.getenv("OPEN_AI")
llm = ChatOpenAI(api_key=OPEN_AI)

class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# Nodes
def chatnode(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

#Checkpointer
checkpointer = InMemorySaver()

# Graph
graph = StateGraph(ChatState)

graph.add_node('chatbot', chatnode)

graph.add_edge(START, 'chatbot')
graph.add_edge('chatbot', END)

chatbot = graph.compile(checkpointer=checkpointer)
