import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from models.job_models import Job
import time
import logging

class JobScraper:
    def __init__(self):
        print("🤖 Inicializando scraper...")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Configura un tiempo de espera implícito
        self.driver.implicitly_wait(10)

    def scrape_linkedin(self, keywords):
        print(f"🔍 Iniciando scraping de LinkedIn...")
        jobs = []
        for keyword in keywords:
            print(f"  Buscando: {keyword}")
            url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location=España"
            
            try:
                # Navegar a la URL
                self.driver.get(url)
                
                # Esperar a que la página cargue completamente
                WebDriverWait(self.driver, 20).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
                
                # Esperar a que los elementos de la página estén presentes
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'job-card-container'))
                )
                
                # Esperar un poco más para asegurar la carga de contenido dinámico
                time.sleep(3)
                
                # Desplazarse por la página para cargar más resultados
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Parsear el contenido
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                # Buscar todos los contenedores de trabajos
                job_containers = soup.find_all('div', class_='job-card-container')
                
                print(f"  📄 Encontrados {len(job_containers)} trabajos para '{keyword}'")
                
                for container in job_containers:
                    try:
                        # Buscar el enlace del trabajo
                        link_elem = container.find('a', class_=['job-card-list__title', 'job-card-list__link'])
                        
                        # Buscar el nombre de la empresa
                        company_elem = container.find('span', class_='job-card-container__primary-description')
                        
                        # Buscar la ubicación
                        location_elem = container.find('span', dir='ltr')
                        
                        # Verificar que todos los elementos existan
                        if link_elem and company_elem and location_elem:
                            title = link_elem.text.strip()
                            company = company_elem.text.strip()
                            location = location_elem.text.strip()
                            link = link_elem['href']
                            
                            job = Job(
                                title=title,
                                company=company,
                                location=location,
                                description="",
                                link=link,
                                platform="LinkedIn"
                            )
                            jobs.append(job)
                    except Exception as e:
                        print(f"  ⚠️ Error procesando una oferta: {str(e)}")
                        continue
            
            except Exception as e:
                print(f"  ❌ Error en scraping de LinkedIn para '{keyword}': {str(e)}")
                continue
                
        print(f"✅ LinkedIn: Encontrados {len(jobs)} trabajos en total")
        return jobs
        
    def scrape_infojobs(self, keywords):
        print(f"🔍 Iniciando scraping de InfoJobs...")
        jobs = []
        for keyword in keywords:
            print(f"  Buscando: {keyword}")
            url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword={keyword}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='ij-OfferCard')
                
                print(f"  📄 Encontrados {len(job_cards)} trabajos para '{keyword}'")
                
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
                    except AttributeError as e:
                        print(f"  ⚠️ Error procesando una oferta: {str(e)}")
                        continue
            else:
                print(f"  ❌ Error obteniendo resultados de InfoJobs. Status code: {response.status_code}")
                    
        print(f"✅ InfoJobs: Encontrados {len(jobs)} trabajos en total")
        return jobs

    def __del__(self):
        print("🤖 Cerrando scraper...")
        self.driver.quit()