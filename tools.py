from pydantic import BaseModel, Field
from typing import Literal


class ToRetrieverAgent(BaseModel):
    """Go to retriever agent to generate the next section"""

    current_section: Literal[
        "title, field_of_invention, background",
        "reference_numbers",
        "brief_description",
        "detailed_description",
        "claims",
        "glossary_of_terms",
        "abstract",
        "other_embodiments",
    ] = Field(
        description="The current_section of the patent report to generate",
    )


class ToFinalReportAgent(BaseModel):
    """Go to final report agent to generate the full final report"""

    report_type: str = Field(
        "patent_report", description="The type of final report to generate"
    )
