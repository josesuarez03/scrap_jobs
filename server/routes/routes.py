from flask import Blueprint, jsonify, request
from models.db_models import MongoDB
from services.scraper import JobScraper
from config import Config
from utils.decorators import log_route
import concurrent.futures
from datetime import datetime, timedelta

jobs_blueprint = Blueprint('jobs', __name__)
mongodb = MongoDB()

@jobs_blueprint.route('/api/jobs/scrape', methods=['POST'])
@log_route
def scrape_jobs():
    db = mongodb.get_db()
    scraper = JobScraper()
    all_jobs = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        linkedin_future = executor.submit(scraper.scrape_linkedin, Config.KEYWORDS)
        infojobs_future = executor.submit(scraper.scrape_infojobs, Config.KEYWORDS)
        
        all_jobs.extend(linkedin_future.result())
        all_jobs.extend(infojobs_future.result())
    
    for job in all_jobs:
        db.jobs.update_one(
            {"link": job.link},
            {"$set": job.to_dict()},
            upsert=True
        )
    
    return jsonify({"message": f"Scraped and saved {len(all_jobs)} jobs"})

@jobs_blueprint.route('/api/jobs', methods=['GET'])
@log_route
def get_jobs():
    db = mongodb.get_db()
    company = request.args.get('company', '')
    location = request.args.get('location', '')
    date_posted = request.args.get('datePosted', '')
    
    query = {}
    if company:
        query['company'] = {'$regex': company, '$options': 'i'}
    if location:
        query['location'] = {'$regex': location, '$options': 'i'}
    if date_posted:
        date_filter = {
            'today': datetime.now() - timedelta(days=1),
            'week': datetime.now() - timedelta(days=7),
            'month': datetime.now() - timedelta(days=30)
        }
        if date_posted in date_filter:
            query['date_posted'] = {'$gte': date_filter[date_posted]}
    
    jobs = list(db.jobs.find(query, {'_id': 0}))
    return jsonify(jobs)