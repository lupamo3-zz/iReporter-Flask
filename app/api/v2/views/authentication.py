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
                        "Ensure you've filled all fields {}".format(data)}, 400
            elif not data['othernames'] or not data['username']:
                return {"message":
                        "Ensure you've filled all fields {}".format(data)}, 400
            elif not data['email'] or not data['phonenumber']:
                return {"message":
                        "Ensure you've filled all fields {}".format(data)}, 400
            elif not data['password']:
                return {"message":
                        "Ensure you've filled all fields {}".format(data)}, 400
        except:
            return {"KeyError": "Kindly check for missing fields"}, 404

        if not re.match(
                r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)", data['email']):
            return {'error': 'Provide a valid email address'}, 400

        elif not str.isalpha(data['username']):
            return {'error':
                    'Username can only contain alphabets'}, 400

        if len(data['password']) < 7:
            return {'error':
                    'Password must be at least 8 characters long!'}, 400
        elif re.search('[0-9]', (data['password'])) is None:
            return {'error':
                    'Password must have at least one number in it!'}, 400
        elif re.search('[A-Z]', (data['password'])) is None:
            return {'error':
                    'Password must have at least one capital letter!'}, 400
        elif re.search('[a-z]', (data['password'])) is None:
            return {'error':
                    'Password must have at least one alphabet letter!'}, 400
        elif re.search(
            '[!,#,$,%,&,*,+,-,<,=,>,?,@,^,_,{,|,},~,]',
                (data['password'])) is None:
            return {'error':
                    'Password must have at least a special character!'}, 400
        elif not len(data['phonenumber'].strip()) == 10:
                return {"error": "phone number must have 10 characters"}, 400
        else:

            firstname = data['firstname'].lower()
            lastname = data['lastname'].lower()
            othernames = data['othernames'].lower()
            username = data['username'].lower()
            email = data['email'].lower()
            phonenumber = data['phonenumber']
            password = generate_password_hash(data['password'])
            isAdmin = data['isAdmin']

            user = self.db.get_username_user(username)
            print(user)
            if user:
                return {"message":
                        "User {} already exists".format(data['username'])
                        }, 400
            else:
                verify_email = self.db.get_user_email(email)
                if verify_email:
                    return {"message":
                            "A user with the email already exists."}, 400

                verify_cell_number = self.db.get_user_cellnumber(phonenumber)
                if verify_cell_number:
                    return {"message":
                            "A user with the phonenumber already exists"}, 400

                sign_up = self.db.save(
                    firstname, lastname, othernames,
                    username, email, phonenumber, password, isAdmin)
                if sign_up:
                    return {"message":
                            "User {} created login ".format(username)}, 201

                return {"Message":
                        "User creation unsuccessful, check data"}, 400


class SignIn(Resource, UsersModel):
    """ Docstring sign in which allows already registered users to sign in """

    def __init__(self):
        self.db = UsersModel()

    def post(self):
        """ Registered user login and validation """
        login_data = request.get_json(force=True)
        try:
            if not login_data:
                return {"message": "Kindly input user info"}, 200
            elif not login_data['username'] or not login_data['password']:
                return {"message":
                        "Ensure youve filled all fields {}".format(login_data)}
        except:
            return {"KeyError": "Kindly check for missing fields"}, 404

        if not login_data:
            return {"Message":
                    "Kindly input Username and Password details"}, 200

        username = login_data['username'].lower()
        password = generate_password_hash(login_data['password'])
        user = self.db.get_username_user(username)

        if not user:
            return {"Message":
                    'User {} doesn\'t exist, Kindly register'.format(
                        login_data['username'])}, 401

        if user:
            if check_password_hash(user[9], login_data['password']):
                access_token = create_access_token(
                    identity=username,
                    expires_delta=datetime.timedelta(minutes=60)
                )
                return {
                    "data":
                        "Logged in as {}".format(login_data['username']),
                        "access_token": access_token

                }, 200

        return {"message": "Wrong credentials, check password!"}, 401
