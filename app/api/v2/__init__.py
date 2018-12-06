from .redflag_views import MyRecords, MyIncidents
from flask_restful import Resource, Api
from flask import Blueprint

version_2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_2)
api.add_resource(MyIncidents, '/incidents')
api.add_resource(MyRecords, '/incidents/<int:id>')
