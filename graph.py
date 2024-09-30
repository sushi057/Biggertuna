import os

from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI

from state import State


graph_builder = StateGraph(State)

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

