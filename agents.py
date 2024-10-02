import os

from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from state import AgentGraphState, get_agent_graph_state
from prompts import (
    planner_prompt_template,
    retriever_prompt_template,
    reviewer_prompt_template,
    quality_control_prompt_template,
    final_report_prompt_template,
)


class Agent:
    def __init__(self, state: AgentGraphState, model=None, temperature=None):
        self.state = state
        self.llm = ChatOpenAI(
            model="gpt-4o-mini", temperature=0.5, api_key=os.getenv("OPENAI_API_KEY")
        )


class PlannerAgent(Agent):
    def invoke(self, next_section=None):
        self.state = {**self.state, "next_section": next_section}

        return self.state


class RetrievalAgent(Agent):
    def invoke(self):
        retriever_runnable = retriever_prompt_template | self.llm
        response = retriever_runnable.invoke(self.state)

        self.state = {**self.state, "messages": response}
        self.state = {**self.state, "current_section_text": response.content}
        return self.state


class ReviewerAgent(Agent):
    def invoke(self):
        reviewer_runnable = reviewer_prompt_template | self.llm
        response = reviewer_runnable.invoke(self.state)

        self.state = {**self.state, "messages": response}
        self.state = {**self.state, "current_section_text": response.content}
        return self.state


class QualityControlAgent(Agent):
    def invoke(self):
        return self.state


class FinalReportAgent(Agent):
    def invoke(self):
        return self.state
