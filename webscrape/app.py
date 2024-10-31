# app.py
from fastapi import FastAPI, HTTPException
from pydantc import BaseModel
from redis import Redis
from rq import Queue
import config

app = FastAPI()

# Redis connection and queue setup
redis_conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
queue = Queue(config.QUEUE_NAME, connection=redis_conn)

# Job request model
class JobRequest(BaseModel):
    brand: str
    model: str
    year: int
    fuelType: str
    transmission: str

@app.post("/submit-job")
async def submit_job(job: JobRequest):
    try:
        job_data = job.dict()
        queue.enqueue('jobs.job_worker.process_job', job_data)
        return {"message": "Job added to queue successfully", "job_data": job_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
