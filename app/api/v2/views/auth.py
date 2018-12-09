import re

from flask_restful import request, Resource
from flask import jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash

from flask_jwt_extended import (jwt_refresh_token_required,
                                JWTManager, jwt_required, create_access_token,
                                get_jwt_identity, create_refresh_token
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
        password = generate_password_hash(data['password'])

        try:
            access_token = create_access_token(identity=data['username']),
            refresh_token = create_refresh_token(identity=data['username'])    
            user = self.db.get_username_user(username)
            if user:
                return make_response(jsonify({
                    "message": "User {} already exists".format(data['username'])
                }))
            sign_up = self.db.save(firstname, lastname, othernames, username,
                                email, phonenumber, password)

            return make_response(jsonify({
                "status": 201,
                "data": [{
                    "access_token": access_token,
                    "refresh_token": resfresh_token,
                    "incident_created": sign_up,
                    "message": "Created {} successfuly, you can now login ".format(username)
                }]
            }), 201)
        except:
            return make_response(jsonify({
                "message": "Check again"
            }), 500)


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

        username = login_data['username']
        password = login_data['password']

        user = self.db.get_username_user(login_data['username'])

        if not user:
            return make_response(jsonify({
                'message': 'User {} doesn\'t exist'.format(
                    login_data['username']
                )
            }))

        if not self.db.login_user():
            access_token = create_access_token(identity=login_data['username'])
            refresh_token = create_refresh_token(identity=login_data['username'])
            return make_response(jsonify({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "status": user,
                "message": "Logged in as {}".format(login_data['username'])
            }), 200)

        return make_response(jsonify({
            "status": 401,
            "message": "Wrong credentials"
        }))
