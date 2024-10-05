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
            """
            You are an assistant for a patent writing company that writes a patent report based on user's requirements and the context provided.
            Use the following pieces of retrieved documents and write a patent report based on user's requirements only for the given sections of the report: {current_section}
            
            Context: {context}
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)

reviewer_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a reviewer for a patent writing company that reviews the item provided to you and makes necessary changes.
            Your responsibility is to review the current section {current_section} of the patent report sent by retriever_agent using the following pieces of information
            
            Context: {context}

            Make necessary changes to the report based on the review.
            Do not generate anything more than the current section.
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)

feedback_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a quality control agent for a patent writing company. 
            You will listen to user's feedback and make changes to the report section accordingly.
            If the user is satisfied with the report, inform the user and go to the retriever agent to generate the next report section.
            If all sections of the report are complete, finally go to the final report agent.
            """,
        ),
        ("placeholder", "{messages}"),
    ]
)

final_report_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a final report agent for a patent writing company. You are responsible for generating the final report for the patent.",
        ),
        ("placeholder", "{messages}"),
    ]
)
