from langchain_core.prompts import ChatPromptTemplate

planner_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a planner agent for a patent writing company. You are responsible for selecting the current section of the patent to work on.",
        )
    ]
)

retriever_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a retrieval agent for a patent writing company. You are responsible for finding and writing the relevant information for the current section of the patent.",
        ),
        ("placeholder", "{current_section}"),
    ]
)

reviewer_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a reviewer agent for a patent writing company. You are responsible for reviewing the current section of the patent.",
        ),
        ("placeholder", "{current_section}"),
    ]
)

quality_control_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a quality control agent for a patent writing company. You are responsible for ensuring the quality of the current section of the patent.",
        ),
        ("placeholder", "{current_section}"),
    ]
)

final_report_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a final report agent for a patent writing company. You are responsible for generating the final report for the patent.",
        )
    ]
)
