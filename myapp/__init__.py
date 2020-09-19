from flask import Flask
from flask_restful import Api


app = Flask(__name__)


class Configuration:
    DEBUG = True


app.config.from_object(Configuration)
api = Api(app)

from .views import *
from .worker import *
