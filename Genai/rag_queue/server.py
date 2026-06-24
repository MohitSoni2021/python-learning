from fastapi import FastAPI, Query
from clients.rq_client import queue
from queues.worker import query_process

app = FastAPI()

@app.get("/")
def root():
    return {"status":200, "msg":"Health is ok..."}

@app.post("/chat")
def chat(
    query:str = Query(..., description="The chat query of the user.")
):
    job = queue.enqueue(query_process, query)

    return { "status":"queued", "job_id":job.id }

@app.get("/job_stats")
def get_result(
        job_id:str = Query(..., description="The queued job id.")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()

    return { "result" : result }

