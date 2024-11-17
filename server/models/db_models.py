from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure  # Cambiado de ConnectionError a ConnectionFailure
from config import Config
import logging

class MongoDB:
    def __init__(self, app=None):
        self.client = None
        self.db = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        try:
            # Conectar a MongoDB
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client.jobs_db
            
            # Crear colecciones si no existen
            if 'jobs' not in self.db.list_collection_names():
                self.db.create_collection('jobs')
                # Crear índices para la colección jobs
                self.db.jobs.create_index([("link", ASCENDING)], unique=True)
                self.db.jobs.create_index([("company", ASCENDING)])
                self.db.jobs.create_index([("date_posted", DESCENDING)])
            
            if 'logs' not in self.db.list_collection_names():
                self.db.create_collection('logs')
                # Crear índices para la colección logs
                self.db.logs.create_index([("timestamp", DESCENDING)])
                self.db.logs.create_index([("route", ASCENDING)])
                self.db.logs.create_index([("status_code", ASCENDING)])
            
            # Verificar la conexión
            self.client.admin.command('ping')
            print("✅ Conexión exitosa a MongoDB")
            print(f"📁 Base de datos: {self.db.name}")
            print(f"📊 Colecciones: {', '.join(self.db.list_collection_names())}")
            
        except ConnectionFailure as e:  # Cambiado aquí también
            print("❌ Error al conectar con MongoDB:")
            print(f"Error: {str(e)}")
            print("Asegúrate de que MongoDB está corriendo en " + Config.MONGO_URI)
            raise e
    
    def get_db(self):
        if self.db is None:  # Cambiado para comparar explícitamente con None
            raise RuntimeError("MongoDB no está inicializada. Asegúrate de llamar a init_app primero.")
        return self.db