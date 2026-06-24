from openai import OpenAI

client = OpenAI(
    api_key="testing_key",
    base_url="http://localhost:11434/v1",
)

def chat_OpenAI_Agent(model:str, messages:list, properties:dict):
    response = client.chat.completions.parse(
        model=model,
        messages=messages,
        **properties
    )
    return response

def ollama_agent(message:list, properties:dict):
    res = client.chat.completions.parse(
        model="qwen2.5:7b",
        messages=message,
        **properties 
    )
    
    return res

