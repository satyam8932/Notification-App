from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
from rq import Queue
from rq.job import Job
from jobs.job_worker import process_job  # Importing process_job directly
import config

app = FastAPI()

# Allowed origins
allowed_origins = [
    "http://localhost:5000"  # For local development
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],
)

# Redis connection and queue setup
redis_conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
queue = Queue(config.QUEUE_NAME, connection=redis_conn)

# Job request model
class JobRequest(BaseModel):
    userId: int
    notificationType: str
    brand: str
    model: str
    yearStart: str
    yearEnd: str
    fuelType: str
    transmission: str
    priceFrom: str
    priceTo: str
    color: str
    bodyType: str
    origin: str
    pageUrl: str
    currentVehicleCount: int

@app.post("/submit-job")
async def submit_job(job: JobRequest):
    try:
        # Remove empty strings and replace with None
        job_data = {key: (value if value != "" else None) for key, value in job.dict().items()}
        # Enqueue the job directly with the function and capture the job instance
        job = queue.enqueue(process_job, job_data)
        return {"message": "Job added to queue successfully", "job_id": job.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-job/{job_id}")
async def delete_job(job_id: str):
    try:
        # Fetch the job using the job ID
        job = Job.fetch(job_id, connection=redis_conn)
        
        # Cancel the job
        job.cancel()
        
        return {"message": "Job deleted successfully", "job_id": job_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found or could not be deleted.")
