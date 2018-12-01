
from flask import Flask
from flask_restful import Api, Resource

# local  imports
from .api.v1.views import MyIncidents, MyRecords


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(MyIncidents, '/incidents')
    api.add_resource(MyRecords, '/incidents/<int:id>')
    return app
