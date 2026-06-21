import base64
from pathlib import Path
from openai import OpenAI

# Connect to Ollama OpenAI-compatible API
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Get path of current script
BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "image.jpeg"  


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# Convert image to base64
image_base64 = encode_image(IMAGE_PATH)


# Send request to Ollama
response = client.chat.completions.create(
    model="qwen2.5vl",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Describe this image in detail"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)