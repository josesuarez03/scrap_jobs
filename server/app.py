from flask import Flask
from flask_cors import CORS
from routes.routes import jobs_blueprint
from config import Config
from models.db_models import MongoDB
from services.scraper import JobScraper
import threading

def background_scraping():
    print("🔄 Iniciando scraping inicial...")
    scraper = JobScraper()
    db = mongodb.get_db()
    
    # Ejecutar scraping
    all_jobs = []
    all_jobs.extend(scraper.scrape_linkedin(Config.KEYWORDS))
    all_jobs.extend(scraper.scrape_infojobs(Config.KEYWORDS))
    
    # Guardar resultados
    for job in all_jobs:
        db.jobs.update_one(
            {"link": job.link},
            {"$set": job.to_dict()},
            upsert=True
        )
    print(f"✅ Scraping inicial completado. {len(all_jobs)} trabajos guardados.")

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Inicializar MongoDB
mongodb = MongoDB()
mongodb.init_app(app)

app.db = mongodb.get_db()

app.register_blueprint(jobs_blueprint)

if __name__ == '__main__':
    # Iniciar scraping en un hilo separado
    scraping_thread = threading.Thread(target=background_scraping)
    scraping_thread.start()
    
    app.run(debug=True)