from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_GENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system",
            "content":"You are a mathematics expert and you only ans questions related to maths"
        },
        {
            "role": "user", 
            "content": "what is 2+2 = "
        }
    ]
)

print(response.choices[0].message.content)