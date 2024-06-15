from flask import Flask
from config import BaseConfig
from flask_migrate import Migrate






app = Flask(__name__,static_folder = BaseConfig.STATIC_FOLDER, template_folder = BaseConfig.TEMPLATE_FOLDER)

app.config.from_object('config.DevConfig')  # traigo las configuraciones de DevConfig

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

from .models.User import db       # importo el db para poder migrar a la base de datos

migrate = Migrate(app, db)                  # realiza las migraciones

from .routers import home

app.register_blueprint(home, url_prefix="/")
