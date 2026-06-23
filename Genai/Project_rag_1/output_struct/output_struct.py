from pydantic import BaseModel, Field
from typing import Optional

class StructuredOutput(BaseModel):
    tool_name: Optional[str] = Field(None, description="name of the tool used from the avaliable tools section -> if you have used any tool to solve the user query, otherwise it should be null")
    
    tool_input: Optional[str] = Field(None, description="the input you want to provide to the tool, it should be in string format -> if you have used any tool to solve the user query, otherwise it should be null")
    
    tool_output: Optional[str] = Field(None, description="the output you got from the tool. -> if you have used any tool to solve the user query, otherwise it should be null")
    
    final_answer: Optional[str] = Field(None, description="the final answer to the user query, it should be in string format -> it should be the answer to the user query based on the output you got from the tool or it should be your final answer to the user query if you have not used any tool to solve the user query.")
    
    is_final: bool = Field(..., description="if you have provided the final answer to the user query, otherwise it should be false.")
    
    is_tool_required: bool = Field(..., description="if you think that the user query requires you to use any of the avaliable tools to solve the user query, otherwise it should be false.")
    
    error_type: Optional[str] = Field(None, description="if there is any error in the tool output, then it should be the type of error, it can be either 'user_error' or 'tool_error' or 'unknown_error', if there is no error in the tool output, then it should be null")

