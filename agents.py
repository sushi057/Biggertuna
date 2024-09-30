import os

from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from state import AgentGraphState, get_agent_graph_state


class Agent:
    def __init__(self, state: AgentGraphState, model=None, temperature=None):
        self.state = state
        self.llm = ChatOpenAI(
            model=model, temperature=temperature, api_key=os.getenv("OPENAI_API_KEY")
        )

    def update_state(self, key, value):
        state = {**self.state, key: value}


class PlannerAgent(Agent):
    def invoke(self, next_section=None):
        self.update_state("current_section", next_section)
        # self.update_status("user_prompt", user_prompt)
        return self.state


class RetrievalAgent(Agent):
    def invoke(self):
        # self.update_state("messages
        return self.state


class ReviewerAgent(Agent):
    def invoke(self):
        return self.state


class QualityControlAgent(Agent):
    def invoke(self):
        return self.state


class FinalReportAgent(Agent):
    def invoke(self):
        return self.state
