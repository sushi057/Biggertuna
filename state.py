from typing import Annotated, TypedDict, Literal
from langgraph.graph.message import add_messages, AnyMessage


class State(TypedDict):
    """
    State of the agent.

    user_prompt: User's prompt to the agent.
    messages: List of messages exchanged between the user and the agent.
    current_section: Current section of the patent application being filled out.
    """

    user_prompt: str
    messages: Annotated[list[AnyMessage], add_messages]
    current_section: Literal[
        "field_of_invention",
        "background",
        "summary",
        "brief_description",
        "detailed_description",
        "claims",
        "abstract",
        "reference_numbers",
        "glossary_of_terms",
        "other_embodiments",
    ]


# user_prompt: """
# review the attachments and write a PPA for the idea of a tilt sensor that attaches to wrestling headgear to help train wrestlers to keep their head up.
# the sensor will attach to the straps of the headgear, have adjustability to set the zero and setpoint positions, and have some kind of auditory and visual and tactile feedback, like vibration.
# Write the sections in the order described in the Rules attachment starting with the background, use the headgear and footwork attachments as examples
# wait for me to type continue before writing each next section.
# """
