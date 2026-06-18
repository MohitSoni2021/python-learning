# zero short prompting

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key="AIzaSyCpFmdwLUy1vF7zWhlgiyOHIjJRw4agjuk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# zero short prompting : giving direct instruction to the model
SYSTEM_PROMPT = "You are a coding expert and you only ans questions related to coding. your name is Flux"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },
        {
            "role": "user", 
            "content": "what is next js, just give me brief"
        }
    ]
)

print(response.choices[0].message.content)