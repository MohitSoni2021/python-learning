# Few short prompting

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(
    api_key="AIzaSyCpFmdwLUy1vF7zWhlgiyOHIjJRw4agjuk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# few short prompting : giving direct instruction to the model with few examples
SYSTEM_PROMPT = """
    you're an expert ai assitant in resollving user query using chain of thought.
    you work on START, PLAN and OUTPUT steps.
    you need to PLAN first what need to be done. The PLAN can be multiple steps.
    Once you think enough plan has been done, finally you can give an OUTPUT. 

    RULES:
    - strictly follow the given JSON output format
    - Only run one step at a time
    - The Sequence of steps is START ( where user give input ), PLAN ( That can be multiple times ), and finallly OUTPUT ( which is going to be displayed to the user )

    Output JSON format : 
    {
        "step": "START" | "PLAN" | "OUTPUT", 
        "content" : "string" 
    }

    EXAMPLE:
    START: hey can you solve 2 + 3 * 5 / 10
    PLAN : {
        "step": "PLAN" , 
        "content" : "User is interested in solving maths problem" 
    }
    PLAN : {
        "step": "PLAN" , 
        "content" : "looking at the problem we should follow the BODMAS method" 
    }
    PLAN : {
        "step": "PLAN" , 
        "content" : "the BODMAS method, is the correct thing to follow up for this question " 
    }
    PLAN : {
        "step": "PLAN" , 
        "content" : "fist we multiply 3*5 which is 15" 
    }
    PLAN : {
        "step": "PLAN" , 
        "content" : "now, the equation become 2 + 15 / 10 " 
    }
    PLAN : {
        "step": "PLAN" , 
        "content" : "we must perform division that is 1.5 " 
    }
    PLAN : {
        "step": "PLAN" , 
        "content" : "now the equation become 2 + 1.5 " 
    }
    PLAN : {
        "step": "PLAN" , 
        "content" : "finally, let's perform the add the output of the equation is 3.5" 
    }
    PLAN : {
        "step": "PLAN" , 
        "content" : "great, we have solved and finally left with 3.5 as ans" 
    }
    OUTPUT : {
        "step" : "OUTPUT",
        "content" : "3.5
    } 
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    response_format={"type" : "json_object"},
    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },
        {
            "role": "user", 
            "content": "hey, write a code to add n numbers in js"
        },
        {
            "role": "assistant",
            "content": json.dumps({
                "step" : "START",
                "content" : "You want a javascript code to add 'n' numbers "
            })
        },
        {
            "role" : "assistant",
            "content" : json.dumps(
                {
                    "step": "PLAN",
                    "content": "The user wants a JavaScript function to add 'n' numbers. I will use the rest parameter (`...numbers`) to accept an arbitrary number of arguments. The `reduce` method will be used for efficient summation."
                }
            )
        }
    ],
)

print(response.choices[0].message.content)