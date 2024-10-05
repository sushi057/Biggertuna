import os

from langchain_core.runnables import Runnable, RunnableConfig
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ToolMessage

from state import AgentGraphState, get_agent_graph_state
from prompts import (
    planner_prompt_template,
    retriever_prompt_template,
    reviewer_prompt_template,
    feedback_prompt_template,
    final_report_prompt_template,
)
from rag import get_retriever, get_rules_retriever, format_docs
from tools import ToRetrieverAgent, ToFinalReportAgent


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
    def invoke(self, current_section: str):
        print("---------Retrieval Agent---------")
        retriever = get_retriever()

        # Create a runnable for the retriever agent
        context_docs = format_docs(retriever.invoke(self.state["messages"][-1].content))

        if (
            hasattr(self.state["messages"][-1], "tool_calls")
            and self.state["messages"][-1].tool_calls
        ):
            tool_call_id = self.state["messages"][-1].tool_calls[0]["id"]
            tool_message = ToolMessage(
                tool_call_id=tool_call_id, content="reference numbers"
            )

            self.state["messages"].append(tool_message)

        retriever_runnable = retriever_prompt_template | self.llm

        response = retriever_runnable.invoke(
            {
                # self.state["messages"][-1].content,
                "context": context_docs,
                "current_section": current_section,
                "messages": self.state["messages"],
            }
        )

        self.state = {**self.state, "messages": response}
        self.state = {**self.state, "current_section_text": response.content}
        return self.state


class ReviewerAgent(Agent):
    def invoke(self, current_section: str):
        print("---------Reviewer Agent---------")
        rules_retriever = get_rules_retriever()

        # Create runnable for the reviewer agent
        context_docs = format_docs(
            rules_retriever.invoke(self.state["messages"][-1].content)
        )
        reviewer_runnable = reviewer_prompt_template | self.llm
        response = reviewer_runnable.invoke(
            {
                "context": context_docs,
                "current_section": current_section,
                "messages": self.state["messages"],
            }
        )

        self.state = {**self.state, "messages": response}
        self.state = {**self.state, "current_section_text": response.content}
        return self.state


class QualityControlAgent(Agent):
    def invoke(self):
        print("---------Quality Control Agent---------")

        llm = self.llm.bind_tools([ToRetrieverAgent, ToFinalReportAgent])
        feedback_runnable = feedback_prompt_template | llm
        response = feedback_runnable.invoke(self.state)

        self.state = {**self.state, "messages": response}
        self.state = {**self.state, "current_section_text": response.content}
        return self.state


class FinalReportAgent(Agent):
    def invoke(self):
        print("---------Final Report Agent---------")

        return self.state
