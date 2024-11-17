from functools import wraps
from flask import request
from datetime import datetime
from models.log_models import Log
from pymongo import MongoClient
from config import Config
import time
import traceback

client = MongoClient(Config.MONGO_URI)
db = client.jobs_db
logs_collection = db.logs

def log_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        
        try:
            # Ejecutar la función de la ruta
            response = f(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Crear log de éxito
            log = Log(
                route=request.path,
                method=request.method,
                status_code=response.status_code,
                message="Request successful",
                execution_time=round(execution_time, 3)
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Crear log de error
            log = Log(
                route=request.path,
                method=request.method,
                status_code=500,
                message="Error during request",
                error=str(e) + "\n" + traceback.format_exc(),
                execution_time=round(execution_time, 3)
            )
            
            # Re-lanzar la excepción
            raise e
        
        finally:
            # Guardar el log en MongoDB
            logs_collection.insert_one(log.to_dict())
            
        return response
    
    return decorated_function