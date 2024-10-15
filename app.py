import uuid
import chainlit as cl
from graph.graph import create_graph

thread_id = str(uuid.uuid4())

graph = create_graph()

config = {"configurable": {"thread_id": thread_id}}

#  Plan report outline
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

# user_prompt = "review the attachments and write a PPA for the idea of a tilt sensor that attaches to wrestling headgear to help train wrestlers to keep their head up.the sensor will attach to the straps of the headgear, have adjustability to set the zero and setpoint positions, and have some kind of auditory and visual and tactile feedback, like vibration."


# @cl.set_starters
# async def set_starters():
#     return [
#         cl.Starter(
#             label="Generate a PPA for a tilt sensor that attaches to wrestling headgear",
#             message="Write a PPA for the idea of a tilt sensor that attaches to wrestling headgear to help train wrestlers to keep their head up.the sensor will attach to the straps of the headgear, have adjustability to set the zero and setpoint positions, and have some kind of auditory and visual and tactile feedback, like vibration.",
#             icon="📝",
#         ),
#         cl.Starter(
#             label="Write a blog post about the future of AI in the legal industry",
#             message="Write a blog post about the future of AI in the legal industry.",
#             icon="📰",
#         ),
#     ]




@cl.on_chat_start
async def on_chat_start():
    initial_prompt = await cl.AskUserMessage(
        "Enter your prompt for your Provisional Patent Application generation: ",
        timeout=3000,
    ).send()

    messages = []
    for event in graph.stream(
        {
            "messages": ("user", initial_prompt["output"]),
            "current_section": report_sections,
        },
        config,
        stream_mode="values",
    ):
        try:
            messages.append(event["messages"][-1].content)
            # await cl.Message(content=event["messages"][-1].content).send()
            # await cl.Message(
            #     content="Review the above message and provide feedback."
            # ).send()
        except Exception as e:
            cl.Message(content="An error occurred: " + str(e)).send()
    await cl.Message(
        content=messages[-1] + "\nReview the above message and provide feedback."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    graph.update_state(
        config, {"messages": [("user", message.content)]}, as_node="feedback_agent"
    )

    messages = []
    for event in graph.stream(
        None,
        config,
        stream_mode="values",
    ):
        # for value in event.values():
        # print("Assistant:", value["messages"].content, "\n")
        event["messages"][-1].pretty_print()
    await cl.Message(content=event["messages"][-1].content).send()
