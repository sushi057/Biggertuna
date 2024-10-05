import os
import uuid
from langchain_core.messages import BaseMessage, ToolMessage
from graph import create_graph

thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": thread_id}}

graph = create_graph()

# Visualize graph
with open("graph_v0.1.png", "wb") as f:
    f.write(graph.get_graph(xray=True).draw_mermaid_png())


report_sections = [
    "title, field_of_invention, background",
    "reference_numbers",
    "brief_description",
    "detailed_description",
    "claims",
    "glossary_of_terms",
    "abstract",
    "other_embodiments",
]
user_prompt = "review the attachments and write a PPA for the idea of a tilt sensor that attaches to wrestling headgear to help train wrestlers to keep their head up.the sensor will attach to the straps of the headgear, have adjustability to set the zero and setpoint positions, and have some kind of auditory and visual and tactile feedback, like vibration."

# Start the graph
for event in graph.stream(
    {
        "messages": ("user", user_prompt),
        "current_section": report_sections,
    },
    config,
    stream_mode="values",
):
    # for value in event.values():
    # print("Assistant:", value["messages"].content, "\n")
    event["messages"][-1].pretty_print()

state = graph.get_state(config)

# Continue human_interrupt
while True:
    user_input = input("User: ")

    graph.update_state(
        config, {"messages": [("user", user_input)]}, as_node="feedback_agent"
    )

    for event in graph.stream(
        None,
        config,
        stream_mode="values",
    ):
        # for value in event.values():
        # print("Assistant:", value["messages"].content, "\n")
        event["messages"][-1].pretty_print()
