from .views.redflag_views import (
        MyRecords, MyIncidents, MySpecificRecords,
        MyCommentRecords
) 
from .views.user_views import MyUsers, MyAdmin
from .views.auth import SignUp, SignIn


from flask_restful import Resource, Api
from flask import Blueprint

version_2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_2)
api.add_resource(MyIncidents, '/incidents')
api.add_resource(MyRecords, '/incidents/<int:id>')
api.add_resource(MySpecificRecords, '/incidents/<int:id>/location')
api.add_resource(MyCommentRecords, '/incidents/<int:id>/comment')
api.add_resource(MyUsers, '/users')
api.add_resource(MyAdmin, '/users/<int:id>')
api.add_resource(SignUp, '/signup')
api.add_resource(SignIn, '/login')
