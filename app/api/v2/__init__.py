from flask_restful import Resource, Api
from flask import Blueprint

from app.api.v2.views.redflag_views import (
    MyRecords, MyIncidents, MySpecificRecords,
    MyCommentRecords
)
from app.api.v2.views.user_views import MyUsers, MyAdmin
from app.api.v2.views.authentication import SignUp, SignIn


version_2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')
api = Api(version_2)
api.add_resource(MyIncidents, '/incidents', strict_slashes=False)
api.add_resource(MyRecords, '/incidents/<int:id>', strict_slashes=False)
api.add_resource(
    MySpecificRecords,
    '/incidents/<int:id>/location',
    strict_slashes=False
)
api.add_resource(
    MyCommentRecords,
    '/incidents/<int:id>/comment',
    strict_slashes=False
)
api.add_resource(MyUsers, '/users', strict_slashes=False)
api.add_resource(MyAdmin, '/users/<int:id>', strict_slashes=False)
api.add_resource(SignUp, '/signup', strict_slashes=False)
api.add_resource(SignIn, '/login', strict_slashes=False)
