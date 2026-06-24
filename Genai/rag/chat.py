from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore

from openai import OpenAI

# Creating vector embeddings...
embedding_model = OllamaEmbeddings(
    model="nomic-embed-text",
)  

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

# taking user input
user_query = input("Ask something ..\t ")

# return relevant chunks from the vector DB
search_res = vector_db.similarity_search(query=user_query)

# creating context 
context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile location: {result.metadata['source']}" for result in search_res ])

# system Prompt
SYSTEM_PROMPT = f"""
    You're a helpfull ai assitant who answers user query based on the avaliable context retrived from the PDF file along with page_contents and page number.

    You should only answer the user based on the following context and navigate the user to open the right page number to know more.

    Context:
    {
        context
    }
"""

client = OpenAI(
    api_key="AIzaSyCpFmdwLUy1vF7zWhlgiyOHIjJRw4agjuk",
    base_url="http://localhost:11434/v1",
)

chat_history = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT 
    },
    {
        "role" : "user",
        "content": user_query
    }
]

response = client.chat.completions.create(
            model="qwen2.5:7b",
            messages=chat_history
        )

print(f"BOT:\t {response.choices[0].message.content}")