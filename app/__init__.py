
from flask import Flask
from flask_restful import Api, Resource

# local  imports
from .api.v1 import version_1 as v1


def create_app():
    app = Flask(__name__)
    app.register_blueprint(v1)
    return app
