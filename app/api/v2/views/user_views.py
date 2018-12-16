from flask import jsonify, make_response
from flask_restful import Resource, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
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
                "data": all_users
            }), 200)

        return {"Error": "No Users found"}, 404


class MyAdmin(Resource, UsersModel):
    """ Docstring for MyUsersSpecific class, this class has methods that allows
    users to get specific users(GET by id), make changes to a
    user(PATCH) and to delete specific (DELETE by id)"""

    def __init__(self):
        self.db = UsersModel()

    @jwt_required
    def delete(self, id):
        """ Docstring for deleting users"""
        current_user = get_jwt_identity()
        app_users = self.db.get_user_id(id)
        if not app_users:
            return {"Error": "User with that id not found"}, 404
        delete_user = self.db.delete_user(id)

        if delete_user:
            return {"id": id, "message": delete_user}, 200
 
    @jwt_required
    def get(self, id):
        """ Admin get a specif user by id """

        app_users = self.db.get_user_id(id)

        if app_users:
            return make_response(jsonify({
                "data": app_users
            }), 200)

        return {"Error": "User id {} id not found" .format(id)}, 200
