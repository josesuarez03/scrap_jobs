from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from services.scraper import JobScraper
from config import Config
import concurrent.futures

jobs_blueprint = Blueprint('jobs', __name__)
client = MongoClient(Config.MONGO_URI)
db = client.jobs_db
jobs_collection = db.jobs

@jobs_blueprint.route('/api/jobs/scrape', methods=['POST'])
def scrape_jobs():
    scraper = JobScraper()
    all_jobs = []
    
    # Ejecutar scraping en paralelo
    with concurrent.futures.ThreadPoolExecutor() as executor:
        linkedin_future = executor.submit(scraper.scrape_linkedin, Config.KEYWORDS)
        infojobs_future = executor.submit(scraper.scrape_infojobs, Config.KEYWORDS)
        
        all_jobs.extend(linkedin_future.result())
        all_jobs.extend(infojobs_future.result())
    
    # Guardar en MongoDB
    for job in all_jobs:
        jobs_collection.update_one(
            {"link": job.link},
            {"$set": job.to_dict()},
            upsert=True
        )
    
    return jsonify({"message": f"Scraped and saved {len(all_jobs)} jobs"})

@jobs_blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    company_filter = request.args.get('company', '')
    
    query = {}
    if company_filter:
        query['company'] = {'$regex': company_filter, '$options': 'i'}
    
    jobs = list(jobs_collection.find(query, {'_id': 0}))
    return jsonify(jobs)