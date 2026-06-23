# Core Modules
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time
from pydantic import BaseModel, Field
from typing import Optional

# created Modules
from prompts.System_prompts import SYSTEM_PROMPT
from Config.openai_client import client
from tools.tool_exporter import avaliable_tools
from Structured_output.pydantic_structure_base import Structured_output

load_dotenv()

chat_history = [
    {
        "role":"system",
        "content":SYSTEM_PROMPT
    },
]

while True:
    user_query = input("👇\n")

    chat_history.append({
        "role" : "user",
        "content" : user_query
    })

    while True:
        response = client.chat.completions.parse(
            model="qwen2.5:7b",
            response_format=Structured_output,
            messages=chat_history
        )

        raw_Result = response.choices[0].message.content
        
        chat_history.append({
            "role" : "assistant",
            "content" : raw_Result
        })

        # parsed_Result = json.loads (raw_Result)
        parsed_Result = response.choices[0].message.parsed

        if parsed_Result.step == "START" :
            # print("🔥 : \t", parsed_Result.get("content"))
            print("🔥 : \t", parsed_Result.content)
            continue

        if parsed_Result.step == "TOOL":
            # tool_to_call = parsed_Result.get("tool")
            # tool_input = parsed_Result.get("input")

            tool_to_call = parsed_Result.tool
            tool_input = parsed_Result.input

            print(f"tool : \t {tool_to_call} || {tool_input}")

            tool_res = avaliable_tools[tool_to_call](tool_input)

            print(f"tool : \t {tool_to_call} || {tool_input} => {tool_res}")
            chat_history.append({
                "role" : "developer",
                "content" : json.dumps({
                    "step": "OBSERVE" ,
                    "tool" : tool_to_call, 
                    "input" : tool_input,
                    "output" : tool_res 
                })
            })

            continue

        if parsed_Result.step == "PLAN" :
            # print("🧠 : \t", parsed_Result.get("content"))
            print("🧠 : \t", parsed_Result.content)
            continue

        if parsed_Result.step  == "OUTPUT" :
            # print("🇮🇳 : \t", parsed_Result.get("content"))
            print("🇮🇳 : \t", parsed_Result.content)
            break

    print("\n\n\n")


