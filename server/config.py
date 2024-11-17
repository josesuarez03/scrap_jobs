import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    KEYWORDS = [
        "becario", "becarios", "prácticas", "practicas", "intern", "internship",
        "informatica", "informática", "desarrollo", "programador", "programación",
        "fullstack", "full stack", "software", "developer", "engineering",
        "junior", "trainee", "estudiante", "recién graduado"
    ]
