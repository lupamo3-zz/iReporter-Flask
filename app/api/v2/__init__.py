from .redflag_views import MyRecords, MyIncidents

from .user_views import MyUsers, MyUsersSpecific


from flask_restful import Resource, Api
from flask import Blueprint

version_2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_2)
api.add_resource(MyIncidents, '/incidents')
api.add_resource(MyRecords, '/incidents/<int:id>')
api.add_resource(MyUsers, '/users')
api.add_resource(MyUsersSpecific, '/users/<int:id>')
