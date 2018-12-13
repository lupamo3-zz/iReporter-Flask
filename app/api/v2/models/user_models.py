from datetime import datetime
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from app.database_config import test_init_db


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class UsersModel():
    """ Docstring for my users model """

    def __init__(self):
        self.db = test_init_db()
        self.registered = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.isAdmin = "isAdmin"

    """ save our users and appendthem to the database """
    def save(self, firstname, lastname, othernames, username, email,
             phonenumber, password):

        user_data = {
            "firstname": firstname,
            "lastname": lastname,
            "othernames": othernames,
            "username": username,
            "email": email,
            "phonenumber": phonenumber,
            "registered": self.registered,
            "isAdmin": False or True,
            "password": password
        }

        inquire = """INSERT INTO users (firstname, lastname,
                 othernames, username, email, phonenumber, registered,
                  isAdmin, password) VALUES (
                  %(firstname)s, %(lastname)s, %(othernames)s, %(username)s,
                  %(email)s, %(phonenumber)s, %(registered)s, %(isAdmin)s,
                   %(password)s)"""
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
                     isAdmin, password FROM users""")
        user_info = currsor.fetchall()
        response = []

        for key, userrecords in enumerate(user_info):
            user_id, firstname, lastname, othernames, username, email, phonenumber, registered, isAdmin, password = userrecords
            user_data = dict(
                user_id=int(user_id),
                firstname=firstname,
                lastname=lastname,
                othernames=othernames,
                username=username,
                email=email,
                phonenumber=phonenumber,
                registered=registered,
                isAdmin=isAdmin,
                password=password
            )
            response.append(user_data)
        return response
        print(response)

    """ get one user's data"""
    def get_user_id(self, id):
        """ Get a user by ID """
        user_connection = self.db
        currsor = user_connection.cursor()
        currsor.execute("""SELECT * FROM users WHERE user_id=%s""", (id, ))

        select_user = currsor.fetchone()

        user_connection.commit()

        if select_user:
            return select_user

    def delete_user(self, user_id):
        user_connection = self.db
        currsor = user_connection.cursor()
        currsor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        user_connection.commit()

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
        user_connection = self.db
        currsor = user_connection.cursor()
        username = request.get_json()['username']
        currsor.execute("SELECT * FROM users WHERE username='" + str(username) + "'")
        user_connection.commit
