import re

from flask_restful import request, Resource
from flask import jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from flask_jwt_extended import create_access_token
from app.api.v2.models.user_models import UsersModel


class SignUp(Resource, UsersModel):
    """ Docstring for signup class, users can signup with iReporter
     and are validated """

    def __init__(self):
        self.db = UsersModel()

    def post(self):
        """ Unregistered User sign up """
        data = request.get_json(force=True)
        try:
            if not data:
                return {"message": "Kindly input user info"}, 200
            elif not data['firstname'] or not data['lastname']:
                return {"message":
                        "Ensure you've filled all field. i.e {}".format(data)}
            elif not data['othernames'] or not data['username']:
                return {"message":
                        "Ensure you've filled all field. i.e {}".format(data)}
            elif not data['email'] or not data['phonenumber']:
                return {"message":
                        "Ensure you've filled all field. i.e {}".format(data)}
            elif not data['password']:
                return {"message":
                        "Ensure you've filled all field. i.e {}".format(data)}
        except:
            return {"KeyError": "Kindly check for missing fields"}, 404

        firstname = data['firstname']
        lastname = data['lastname']
        othernames = data['othernames']
        username = data['username']
        email = data['email']
        phonenumber = data['phonenumber']
        password = generate_password_hash(data['password'])

        user = self.db.get_username_user(username)
        print(user)
        if user:
            return {"message":
                    "User {} already exists".format(data['username'])
                    }, 400

        sign_up = self.db.save(firstname, lastname, othernames, username,
                               email, phonenumber, password)
        if sign_up:
            return {"message":
                    "User {} created, now login ".format(username)}, 201

        return {"Message": "User creation not successful, check data"}, 400


class SignIn(Resource, UsersModel):
    """ Docstring sign in which allows already registered users to sign in """

    def __init__(self):
        self.db = UsersModel()

    def post(self):
        """ Registered user login and validation """
        login_data = request.get_json(force=True)
        if not login_data:
            return {"Message":
                    "Kindly input Username and Password details"}, 200

        username = login_data['username']
        password = generate_password_hash(login_data['password'])
        user = self.db.get_username_user(username)
        user_id = user[0]

        if not user:
            return {"Message":
                    'User {} doesn\'t exist, Kindly register'.format(
                        login_data['username'])}, 401

        if user:
            if check_password_hash(user[9], login_data['password']):
                access_token = create_access_token(
                    identity=user_id,
                    expires_delta=datetime.timedelta(minutes=60)
                )
                return {
                    "data":
                        "Logged in as {}".format(login_data['username']),
                        "access_token": access_token

                }, 200

        return {"message": "Wrong credentials, check password!"}, 401
