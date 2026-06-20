from fastapi import FastAPI, Body
from ollama import Client

app = FastAPI()

client = Client(
    host="http://localhost:11434"
)

@app.get("/")
def health_checker():
    return {
        "status" : 200,
        "msg" : "The health is ok...."
    }

@app.post('/chat')
def chat(
    message: str = Body(..., description="The message")
):
    response = client.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role":"user",
                "content" : message
            }
        ]
    )

    return {
        "response" : response.message.content
    }