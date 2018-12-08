from flask import jsonify, make_response
from flask_restful import Resource, Api, request

from .user_models import UsersModel


class MyUsers(Resource, UsersModel):
    """ Docstring for MyUsers class, MyUsers class has methods
      to Create Users(POST) and to get all users(GET)"""

    def __init__(self):
        self.db = UsersModel()

    def post(self):
        """ Create a user record """
        data = request.get_json(force=True)

        firstname = data['firstname']
        lastname = data['lastname']
        othernames = data['othernames']
        username = data['username']
        email = data['email']
        phonenumber = data['phonenumber']

        rels = self.db.save(firstname, lastname, othernames, username, email, phonenumber)
        return make_response(jsonify({
            "status": 201,
            "data": [{
                "incident_created": rels,
                "message": "Created user successfuly "
            }]
        }), 201)

    def get(self):
        """ Get all user records """
        all_users = self.db.get_users()

        if all_users:

            return make_response(jsonify({
                "status": 200,
                "data": all_users
            }), 200)

        return make_response(jsonify({
            "status": 404,
            "error": "No Users found"
        }))


class MyUsersSpecific(Resource, UsersModel):
    """ Docstring for MyUsersSpecific class, this class has methods that allows
    users to get specific users(GET by id), make changes to a
    user(PATCH) and to delete specific (DELETE by id)"""

    def __init__(self):
        self.db = UsersModel()

    def get(self, id):
        """ Get a specific user """
        app_users = self.db.get_users()
        for i in app_users:
            if i['user_id'] == id:

                return make_response(jsonify({
                    "status": 200,
                    "data": i
                }), 200)

        return make_response(
            jsonify(
                {
                    "status": 404,
                    "error": "User with that id not found"
                }
            )
        )

    def delete(self, id):
        """ Allows you to delete a user  """
        deleting = self.db.delete_user(id)

        if deleting:
            return make_response(jsonify({
                'status': 200,
                "data": [{
                    "id": id,
                    "message": "User with that record has been deleted"
                }]
            }))
        return make_response(jsonify({
            'status': 200,
            "data": [{
                "id": id,
                'message': 'User not found'
            }]
        }), 404)