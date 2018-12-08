
from flask import Flask
from flask_restful import Api, Resource


# # local  imports
from instance.config import app_config
# from .database_config import create_tables
# create_tables()


def create_app():
    app = Flask(__name__)

    from .api.v1 import version_1 as v1
    app.register_blueprint(v1)

    from .api.v2 import version_2 as v2
    app.register_blueprint(v2)

    return app
