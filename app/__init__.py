
from flask import Flask
from flask_restful import Api, Resource


from .api.v1 import version_1 as v1


# # local  imports
from instance.config import app_config
from .database_config import create_tables


def create_app():
    app = Flask(__name__)
    create_tables()
    app.register_blueprint(v1)
    return app
