import time
import logging
from rq import Queue, Worker, Retry
from redis import Redis
from scraper.car_scraper import scrape_starter
from utils.notifications import send_notification
import config

# Set up Redis connection and queue
redis_conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
job_queue = Queue(config.QUEUE_NAME, connection=redis_conn)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_job(job_data):
    """
    Processes the job by scraping based on job_data (filters).
    Sends notification if listing is available, otherwise re-enqueues.
    """
    logger.info("Processing job with data: %s", job_data)

    # Perform the scraping job
    results = scrape_starter(job_data)

    # Check results and act accordingly
    if results["status"] == "available":
        # Job is successful; send a success notification
        logger.info("Job successful - item available.")
        send_notification({
            "status": "available",
            "listings": results["listings"],
            "newVehicleCount": results["newVehicleCount"],
            "pageUrl": results["page_url"]
        })
        # Re-enqueue the job for future processing
        job_queue.enqueue(process_job, job_data, retry=Retry(max=3, interval=[120]))

    elif results["status"] == "not_available":
        # Job is not successful; send a "not available" notification
        logger.info("Job not available - re-enqueuing job for later processing.")
        send_notification({
            "status": "not_available",
            "message": results["message"],
        })
        # Re-enqueue the job for future processing
        job_queue.enqueue(process_job, job_data, retry=Retry(max=3, interval=[120]))

    elif results["status"] == "warning":
        # Handle any warnings
        logger.warning("Job encountered a warning: %s", results["message"])
        send_notification({
            "status": "warning",
            "message": results["message"],
        })

if __name__ == "__main__":
    logger.info("Starting worker to process jobs from the queue.")
    # Set up a worker to process jobs from the queue
    worker = Worker([job_queue], connection=redis_conn)
    worker.work(with_scheduler=True)
