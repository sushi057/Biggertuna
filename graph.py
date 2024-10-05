import os

from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from state import AgentGraphState, get_agent_graph_state
from agents import (
    RetrievalAgent,
    ReviewerAgent,
    QualityControlAgent,
    FinalReportAgent,
)


def route_quality_control_agent(state: AgentGraphState):
    messages = state["messages"]
    if not hasattr(messages[-1], "tool_calls") or not messages[-1].tool_calls:
        return "quality_control_agent"
    elif messages[-1].tool_calls[0]["name"] == "ToRetrieverAgent":
        return "retriever_agent"
    elif not state["current_section"]:
        return "final_report_agent"


def create_graph():
    graph_builder = StateGraph(AgentGraphState)
    graph_builder.add_node(
        "retriever_agent",
        lambda state: RetrievalAgent(state).invoke(
            current_section=state["current_section"][0]
        ),
    )
    graph_builder.add_node(
        "reviewer_agent",
        lambda state: ReviewerAgent(state).invoke(
            current_section=state["current_section"][0]
        ),
    )
    graph_builder.add_node(
        "quality_control_agent",
        lambda state: QualityControlAgent(
            state,
        ).invoke(),
    )
    graph_builder.add_node(
        "final_report_agent", lambda state: FinalReportAgent(state).invoke()
    )

    # graph_builder.add_edge(START, "planner_agent")
    graph_builder.add_edge(START, "retriever_agent")
    graph_builder.add_edge("retriever_agent", "reviewer_agent")
    graph_builder.add_edge("reviewer_agent", "quality_control_agent")
    graph_builder.add_conditional_edges(
        "quality_control_agent",
        route_quality_control_agent,
        {
            "retriever_agent": "retriever_agent",
            "final_report_agent": "final_report_agent",
            "quality_control_agent": "quality_control_agent",
            # "__end__": "__end__",
        },
    )
    graph_builder.add_edge("final_report_agent", END)

    memory = MemorySaver()
    graph = graph_builder.compile(
        checkpointer=memory,
        interrupt_before=["quality_control_agent"],
    )
    return graph
