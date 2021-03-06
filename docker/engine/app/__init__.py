
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, uuid
from flasgger import Swagger
from engine.app.schemas import ma
from engine.app.utils import register_error_handlers

basedir = os.path.abspath(os.path.dirname(__file__))


ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

app = Flask(__name__)

if os.environ["FLASK_ENV"] == 'testing':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = str(uuid.uuid4())

db = SQLAlchemy(app)
Swagger(app, template_file='swagger.yaml')

from engine.app.models import *
from engine.app.resources import *

Migrate(app, db)


def create_app():
    from engine.app.resources.api import api
    app.register_blueprint(api)
    register_error_handlers(app)
    ma.init_app(app)
    return app
