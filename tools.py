from pydantic import BaseModel, Field


class ToRetrieverAgent(BaseModel):
    """Go to retriever agent to generate the next section"""

    current_section: str = Field(
        descroption="The current_section of the patent report to generate"
    )


class ToFinalReportAgent(BaseModel):
    """Go to final report agent to generate the full final report"""

    report_type: str = Field(
        "patent_report", description="The type of final report to generate"
    )
