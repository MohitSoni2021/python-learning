from fastapi import FastAPI, Query
from queue_client.main import queue
from langgraph_flow.worker import init_chatbot


app = FastAPI()

@app.get("/")
def root():
    return {"status":200, "msg":"The server is properly running..."}

@app.post("/chat")
def chat(
    query: str = Query(..., description="User query for llm."), 
    user_id: str = None
):
    if user_id is None:
        return {"status":400, "msg":"user_id is required."}
    
    job = queue.enqueue(init_chatbot, query)
    return {"status":200, "job_id": job.id}


@app.post("/chat-adv")
def chat_adv(
    query: str = Query(..., description="User query for llm."),
    user_id: str = None
):
    if user_id is None:
        return {"status":400, "msg":"user_id is required."}

    result = init_chatbot(query)
    return {"status":200, "result": result}

@app.get("/job_stats")
def get_result(
        job_id:str = Query(..., description="The queued job id.")
):
    job = queue.fetch_job(job_id=job_id)
    print("🏢 : \t", job)
    result = job.return_value()

    return { "result" : result }

    