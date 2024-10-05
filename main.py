import os
import uuid
from langchain_core.messages import BaseMessage, ToolMessage
from graph import create_graph

thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": thread_id}}

graph = create_graph()

# Visualize graph
# with open("graph_v0.1.png", "wb") as f:
#     f.write(graph.get_graph(xray=True).draw_mermaid_png())


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

# while True:
#     user_input = input("User: ")

#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Goodbye!")
#         break

#     for event in graph.stream({"messages": [("user", user_input)]}, config):
#         for value in event.values():
#             print("Assistant:", value["messages"] + "\n")

for event in graph.stream(
    {
        "messages": ("user", user_prompt),
        "current_section": ["title, field of invention and background"],
    },
    config,
    stream_mode="values",
):
    # for value in event.values():
    # print("Assistant:", value["messages"].content, "\n")
    event["messages"][-1].pretty_print()

state = graph.get_state(config)
# print(state)
while True:
    # user_input = input("User: ")

    # if hasattr(state[0]["messages"][-1], "tool_calls") and state[0]["messages"][-1].tool_calls:
    #     tool_call_id = graph.get_state(config)[0]["messages"][-1].tool_calls[0][
    #         "id"
    #     ]
    #     tool_message = [
    #         {"tool_call_id": tool_call_id, "content": user_input, "type": "tool"}
    #     ]
    #     graph.update_state(config, {"messages": tool_message})

    graph.update_state(
        config, {"messages": [("user", "looks good")]}, as_node="feedback_agent"
    )

    for event in graph.stream(
        None,
        config,
        stream_mode="values",
    ):
        # for value in event.values():
        # print("Assistant:", value["messages"].content, "\n")
        event["messages"][-1].pretty_print()
