from openai import OpenAI
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

from prompts.system_prompt import SYSTEM_PROMPT

# OpenAI connection
openai_client = OpenAI(
    api_key="AIzaSyCpFmdwLUy1vF7zWhlgiyOHIjJRw4agjuk",
    base_url="http://localhost:11434/v1",
)

# Creating vector embeddings...
embedding_model = OllamaEmbeddings(
    model="nomic-embed-text",
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

def query_process(query : str) :
    print(f"Searching Chunks : ", query)
    search_res = vector_db.similarity_search(query=query)

    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile location: {result.metadata['source']}" for result in search_res ])

    system_prompt = SYSTEM_PROMPT(context=context)

    chat_history = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role" : "user",
            "content": query
        }
    ]

    response = openai_client.chat.completions.create(
        model="qwen2.5:7b",
        messages=chat_history
    )

    print(f"BOT:\t {response.choices[0].message.content}")
    return response.choices[0].message.content

