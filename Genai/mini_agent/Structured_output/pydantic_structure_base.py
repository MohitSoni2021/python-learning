from pydantic import BaseModel, Field
from typing import Optional

class Structured_output(BaseModel):
    step : str = Field(..., description="The ID of the step. It can be START | PLAN | OUTPUT | TOOL | OBSERVE.") 
    content : Optional[str] = Field(None, description="Optional string content for the step.")
    tool : Optional[str] = Field(None, description="The ID of the tool to call.")
    input : Optional[str] = Field(None, description="The input params for the tools.")
    output : Optional[str] = Field(None, description="The response from the tool.")