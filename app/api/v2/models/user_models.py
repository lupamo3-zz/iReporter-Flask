from datetime import datetime
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database_config import test_init_db


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class UsersModel():
    """ Docstring for my users model """

    def __init__(self):
        self.db = test_init_db()
        self.registered = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.isAdmin = False

    """ save our users and appendthem to the database """
    def save(self, firstname, lastname, othernames, username, email,
             phonenumber, password):
        try:
            user_data = {
                "firstname": firstname,
                "lastname": lastname,
                "othernames": othernames,
                "username": username,
                "email": email,
                "phonenumber": phonenumber,
                "registered": self.registered,
                "password": password,
                "isAdmin": self.isAdmin
            }
        except KeyError:
            return False, "Missing fields"

        inquire = """INSERT INTO users (firstname, lastname,
                 othernames, username, email, phonenumber, registered,
                  password, isAdmin) VALUES (
                  %(firstname)s, %(lastname)s, %(othernames)s, %(username)s,
                  %(email)s, %(phonenumber)s, %(registered)s,
                   %(password)s, %(isAdmin)s)"""
        currsor = self.db.cursor()
        currsor.execute(inquire, user_data)
        self.db.commit()
        return user_data

    """get all the users """
    def get_users(self):

        user_connection = self.db
        currsor = user_connection.cursor()
        currsor.execute("""SELECT user_id, firstname, lastname,
                     othernames, username, email, phonenumber, registered,
                     isAdmin FROM users""")
        user_info = currsor.fetchall()
        response = []

        for key, userrecords in enumerate(user_info):
            user_id, firstname, lastname, othernames, username, email, phonenumber, registered, isAdmin = userrecords
            user_data = dict(
                user_id=int(user_id),
                firstname=firstname,
                lastname=lastname,
                othernames=othernames,
                username=username,
                email=email,
                phonenumber=phonenumber,
                registered=registered,
                isAdmin=isAdmin
            )
            response.append(user_data)
        return response

    """ get one user's data"""
    def get_user_id(self, id):
        """ Get a user by ID """
        user_connection = self.db
        print(user_connection)
        currsor = user_connection.cursor()
        currsor.execute("""SELECT * FROM users WHERE user_id=%s""", (id, ))

        select_user = currsor.fetchone()

        user_connection.commit()

        if select_user:
            return select_user

    def delete_user(self, id):
        """ To delete user and user details """
        user_connection = self.db
        currsor = user_connection.cursor()
        currsor.execute("DELETE FROM users WHERE user_id = %s", (id,))
        user_connection.commit()
        return "User of that record has been deleted"

    def get_username_user(self, username):
        """ Get user by username """
        user_connection = self.db
        currsor = user_connection.cursor()
        currsor.execute("""SELECT * FROM users WHERE username=%s""", (username, ))
        select_user = currsor.fetchone()
        user_connection.commit()
        if select_user:
            return select_user

    def login_user(self):
        """ User login validation """
        user_connection = self.db
        currsor = user_connection.cursor()
        username = request.get_json()['username']
        currsor.execute("SELECT * FROM users WHERE username='" + str(username) + "'")
        user_connection.commit()
