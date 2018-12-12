import re

from flask_restful import request, Resource
from flask import jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash

from flask_jwt_extended import create_access_token

from ..models.user_models import UsersModel


class SignUp(Resource, UsersModel):
    """ Docstring for signup class, users can signup with iReporter
     and are validated """

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
            access_token = create_access_token(identity=data['username'])
            user = self.db.get_username_user(username)
            if user:
                return make_response(
                    jsonify({
                        "message":
                        "User{} already exists".format(data['username'])
                    }), 404)
            sign_up = self.db.save(firstname, lastname, othernames, username,
                                   email, phonenumber, password)

            return make_response(jsonify({
                "status": 201,

                "access_token": access_token,
                "message":
                "Created {} successfuly, you can now login ".format(username)
            }), 201)
        except:
            return make_response(jsonify({
                "message": "User creation not successful"
            }), 400)


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
            }), 200)

        username = login_data['username']
        password = login_data['password']
        user = self.db.get_username_user(username)

        if not user:
            return make_response(jsonify({
                'message': 'User {} doesn\'t exist, Kindly register'.format(
                    login_data['username']
                )
            }))

        if user:
            if check_password_hash(login_data['password'], password):

                access_token = create_access_token(
                    identity=login_data['username'],
                    expires_delta=False
                    )
                return make_response(jsonify({
                    "access_token": access_token,
                    "message": "Logged in as {}".format(login_data['username'])
                }), 200)

            return make_response(jsonify({
                "status": 400,
                "message": "Wrong credentials"
            }))
