from .views import MyRecords, MyIncidents
from flask_restful import Resource, Api
from flask import Blueprint

version_1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(version_1)
api.add_resource(MyIncidents, '/incidents', strict_slashes=False)
api.add_resource(MyRecords, '/incidents/<int:id>', strict_slashes=False)
