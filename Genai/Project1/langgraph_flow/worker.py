from openai import OpenAI
from langchain_ollama import OllamaEmbeddings
from langchain_qdrant import QdrantVectorStore
# from ..prompts.system_prompt import SYSTEM_PROMPT
from typing_extensions import TypedDict
from typing import Annotated, Optional, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCpFmdwLUy1vF7zWhlgiyOHIjJRw4agjuk",
    base_url="http://localhost:11434/v1",
)

# Creating vector embeddings... and Vector DB connection.
embedding_model = OllamaEmbeddings(
    model="nomic-embed-text",
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag"
)

class State(TypedDict):
    user_query : str
    llm_output: Optional[str]
    is_good: Optional[bool]

# This chatbot fun define the whole process
# user_query -> getting context over user query -> llm(processing -> context over user query) -> return state.
def chatbot(state: State):
    user_query = state.get("user_query")

    # getting the info from vectorDB using similarity search.
    search_res = vector_db.similarity_search(query=user_query)

    # creating context for the llm.
    context = "\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile location: {result.metadata['source']}" for result in search_res ])

    system_prompt = f"""
        You're a helpfull ai assitant who answers user query based on the avaliable context retrived from the PDF file along with page_contents and page number.

        You should only answer the user based on the following context and navigate the user to open the right page number to know more.

        Context:
        {
            context
        }
    """

    # # getting the system_prompt.
    # system_prompt = SYSTEM_PROMPT(context=context)

    # getting the response over the context from the vectorDB on the user query.
    response = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content":user_query}
        ]
    )

    state["llm_output"] = response.choices[0].message.content
    return state

def endnode(state: State):
    return state



graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "endnode")
graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

# this is the starting point of the agent workflow.
def init_chatbot(query:str):
    updated_state = graph.invoke(State({ "user_query": f"\n\n{query}" }))
    # print(f"\n💻️ : \t {updated_state["llm_output"]}")
    return updated_state["llm_output"]


# getting_user_query_input = input("👉️ : \t")

# init_chatbot(getting_user_query_input)