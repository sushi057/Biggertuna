import os

from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

from state import AgentGraphState, get_agent_graph_state
from agents import (
    RetrievalAgent,
    ReviewerAgent,
    FeedbackAgent,
    FinalReportAgent,
)


def route_feedback_agent(state: AgentGraphState):
    messages = state["messages"]
    if not hasattr(messages[-1], "tool_calls") or not messages[-1].tool_calls:
        return "feedback_agent"
    elif messages[-1].tool_calls[0]["name"] == "ToRetrieverAgent":
        return "retriever_agent"
    elif not state["current_section"]:
        return "final_report_agent"
        # tool_call_id = messages[-1].tool_calls[0]["id"]
        # tool_message = [
        #     {
        #         "tool_call_id": tool_call_id,
        #         "content": "reference numbers",
        #         "type": "tool",
        #     }
        # ]
        # state = {**state, "messages": tool_message}


def create_graph():
    graph_builder = StateGraph(AgentGraphState)
    graph_builder.add_node(
        "retriever_agent",
        lambda state: RetrievalAgent(state).invoke(
            current_section=(
                state["current_section"][0]
                if state["current_section"]
                else "final_embodiments"
            )
        ),
    )
    graph_builder.add_node(
        "reviewer_agent",
        lambda state: ReviewerAgent(state).invoke(
            current_section=state["current_section"][0]
        ),
    )
    graph_builder.add_node(
        "feedback_agent",
        lambda state: FeedbackAgent(
            state,
        ).invoke(),
    )
    graph_builder.add_node(
        "final_report_agent", lambda state: FinalReportAgent(state).invoke()
    )

    # graph_builder.add_edge(START, "planner_agent")
    graph_builder.add_edge(START, "retriever_agent")
    graph_builder.add_edge("retriever_agent", "reviewer_agent")
    graph_builder.add_edge("reviewer_agent", "feedback_agent")
    graph_builder.add_conditional_edges(
        "feedback_agent",
        route_feedback_agent,
        {
            "retriever_agent": "retriever_agent",
            "final_report_agent": "final_report_agent",
            "feedback_agent": "feedback_agent",
            # "__end__": "__end__",
        },
    )
    graph_builder.add_edge("final_report_agent", END)

    memory = MemorySaver()
    graph = graph_builder.compile(
        checkpointer=memory,
        interrupt_before=["feedback_agent"],
    )
    return graph
