from flask import jsonify, make_response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required

from app.api.v2.models.user_models import UsersModel


class MyUsers(Resource, UsersModel):
    """ Docstring for MyUsers class, MyUsers class has methods
      to Create Users(POST) and to get all users(GET)"""

    def __init__(self):
        self.db = UsersModel()

    @jwt_required
    def get(self):
        """ Get all user records """
        all_users = self.db.get_users()

        if all_users:

            return make_response(jsonify({
                "status": 200,
                "data": all_users
            }), 200)

        return {"data": [{"error": "No Users found"}]}, 404


class MyAdmin(Resource, UsersModel):
    """ Docstring for MyUsersSpecific class, this class has methods that allows
    users to get specific users(GET by id), make changes to a
    user(PATCH) and to delete specific (DELETE by id)"""

    def __init__(self):
        self.db = UsersModel()

    # @jwt_required
    # def delete(self, id):

    #     delete_user = self.db.delete_user(id)

    #     if delete_user:
    #         return make_response(jsonify({
    #             'status': 200,
    #             "data": [{
    #                 "id": id,
    #                 "message": "User with that record has been deleted"
    #             }]
    #         }))
    #     return make_response(jsonify({
    #         'status': 200,
    #         "data": [{
    #             "id": id,
    #             'message': 'User not found'
    #         }]
    #     }), 404)

    @jwt_required
    def get(self, id):
        """ Admin get a specif user by id """

        app_users = self.db.get_user_id(id)

        if app_users:
            return make_response(jsonify({
                "status": 200,
                "data": app_users
            }), 200)

        return {"data": [{"error": "User with that id not found"}]}, 200
