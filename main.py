import os
import uuid
from langchain_core.messages import BaseMessage
from graph import create_graph

thread_id = str(uuid.uuid4())

config = {"configurable": {"thread_id": thread_id}}

graph = create_graph()

# Visualize graph
with open("graph_v0.1.png", "wb") as f:
    f.write(graph.get_graph(xray=True).draw_mermaid_png())

conversation = [
    "hi",
    "review the attachments and write a PPA for the idea of a tilt sensor that attaches to wrestling headgear to help train wrestlers to keep their head up.the sensor will attach to the straps of the headgear, have adjustability to set the zero and setpoint positions, and have some kind of auditory and visual and tactile feedback, like vibration.Write the sections in the order described in the Rules attachment starting with the background, use the headgear and footwork attachments as exampleswait for me to type continue before writing each next section.",
]

# while True:
#     user_input = input("User: ")

#     if user_input.lower() in ["quit", "exit", "q"]:
#         print("Goodbye!")
#         break

#     for event in graph.stream({"messages": [("user", user_input)]}, config):
#         for value in event.values():
#             print("Assistant:", value["messages"][-1].content + "\n")

for event in graph.stream({"messages": "hi"}, config):
    for value in event.values():
        print("Assistant:", value["messages"], "\n")
