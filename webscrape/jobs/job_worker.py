# jobs/job_worker.py
from scraper.car_scraper import scrape_cars
from utils.notifications import send_notification

def process_job(job_data):
    # Process the job by scraping based on job_data (filters)
    results = scrape_cars(job_data)
    if results:
        send_notification(results)
