from flask import Flask
from flask_restful import Api

from . import config

app = Flask(__name__)

app.config.from_object(config.Configuration)
api = Api(app)

from . import views, app
from .models import Url, db
from .worker import celery
