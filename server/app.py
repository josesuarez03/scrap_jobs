from flask import Flask
from flask_cors import CORS
from routes.routes import jobs_blueprint
from config import Config
from models.db_models import MongoDB

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Inicializar MongoDB
mongodb = MongoDB()
mongodb.init_app(app)

# Hacer la instancia de db disponible globalmente
app.db = mongodb.get_db()

app.register_blueprint(jobs_blueprint)

if __name__ == '__main__':
    app.run(debug=True)