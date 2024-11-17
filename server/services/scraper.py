import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from models.db_models import Job
import time

class JobScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape_linkedin(self, keywords):
        jobs = []
        for keyword in keywords:
            url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location=España"
            self.driver.get(url)
            time.sleep(2)  # Esperar a que cargue el contenido dinámico
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            job_cards = soup.find_all('div', class_='job-card-container')
            
            for card in job_cards:
                try:
                    title = card.find('h3', class_='job-card-title').text.strip()
                    company = card.find('h4', class_='job-card-company-name').text.strip()
                    location = card.find('span', class_='job-card-location').text.strip()
                    link = card.find('a', class_='job-card-link')['href']
                    
                    job = Job(
                        title=title,
                        company=company,
                        location=location,
                        description="",  # Se podría obtener entrando en cada oferta
                        link=link,
                        platform="LinkedIn"
                    )
                    jobs.append(job)
                except AttributeError:
                    continue
                
        return jobs

    def scrape_infojobs(self, keywords):
        jobs = []
        for keyword in keywords:
            url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={keyword}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='ij-OfferCard')
                
                for card in job_cards:
                    try:
                        title = card.find('h2', class_='ij-OfferCard-title').text.strip()
                        company = card.find('a', class_='ij-OfferCard-companyName').text.strip()
                        location = card.find('span', class_='ij-OfferCard-location').text.strip()
                        link = card.find('a', class_='ij-OfferCard-title')['href']
                        
                        job = Job(
                            title=title,
                            company=company,
                            location=location,
                            description="",
                            link=link,
                            platform="InfoJobs"
                        )
                        jobs.append(job)
                    except AttributeError:
                        continue
                    
        return jobs

    def __del__(self):
        self.driver.quit()