
import os


from flask import Flask
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager


# # local  imports
from instance.config import app_config
from .database_config import create_tables
create_tables()


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    from .api.v1 import version_1 as v1
    app.register_blueprint(v1)

    from .api.v2 import version_2 as v2
    app.register_blueprint(v2)

    return app

