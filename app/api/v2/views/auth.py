import re

from flask_restful import request, Resource
from flask import jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from ..models.user_models import UsersModel


class SignUp(Resource, UsersModel):
    """ Docstring for signup class, users can signup with iReporter and are 
                      validated """

    def __init__(self):
        self.db = UsersModel()

    def post(self):
        """ Unregistered User sign up """
        data = request.get_json(force=True)
        if not data:
            return make_response(jsonify({
                "status": 200,
                "message": "Kindly input user information"
            }), 200)

        firstname = data['firstname']
        lastname = data['lastname']
        othernames = data['othernames']
        username = data['username']
        email = data['email']
        phonenumber = data['phonenumber']
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            return make_response(jsonify({
                "data": 400,
                "message": "Passwords not matching"
            }))

        user = self.db.get_username_user(username)
        if user:
            return make_response(jsonify({
                "message": "User {} already exists".format(data['username'])
            }))
        sign_up = self.db.save(firstname, lastname, othernames, username,
                               email, phonenumber, password, confirm_password)

        return make_response(jsonify({
            "status": 201,
            "data": [{
                "incident_created": sign_up,
                "message": "Created {} successfuly, you can now login ".format(username)
            }]
        }), 201)


class SignIn(Resource, UsersModel):
    """ Docstring sign in which allows already registered users to sign in """

    def __init__(self):
        self.db = UsersModel()

    def post(self):
        """ Registered user login and validation """
        login_data = request.get_json(force=True)
        if not login_data:
            return make_response(jsonify({
                "status": 200,
                "message": "Kindly input Username and Password details"
            }), 404)
        # username = login_data['username']
        # password = login_data['password']

        user = self.db.get_username_user(login_data['username'])

        if not user:
            return make_response(jsonify({
                'message': 'User {} doesn\'t exist'.format(
                    login_data['username']
                )
            }))

        # access_token = create_access_token(identity=username)
        if login_data['password'] == login_data['username']:
            return make_response(jsonify({
                # "access_token": access_token,
                "status": user,
                "message": "Logged in as {}".format(user.username)
            }), 200)

        return make_response(jsonify({
            "status": 401,
            "message": "Wrong credentials"
        }))
