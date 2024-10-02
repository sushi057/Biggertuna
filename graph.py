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


def create_graph():
    graph_builder = StateGraph(AgentGraphState)

    # graph_builder.add_node(
    #     "planner_agent",
    #     lambda state: PlannerAgent(
    #         state,
    #     ).invoke(),
    # )

    graph_builder.add_node(
        "reviewer_agent", lambda state: ReviewerAgent(state).invoke()
    )

    graph_builder.add_node(
        "retriever_agent", lambda state: RetrievalAgent(state).invoke()
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
    graph_builder.add_edge("quality_control_agent", "final_report_agent")
    graph_builder.add_edge("final_report_agent", END)

    memory = MemorySaver()
    graph = graph_builder.compile(
        checkpointer=memory,
    )
    return graph
