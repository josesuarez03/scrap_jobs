from flask import Flask
from flask_cors import CORS
from routes.routes import jobs_blueprint
from config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

app.register_blueprint(jobs_blueprint)

if __name__ == '__main__':
    app.run(debug=True)