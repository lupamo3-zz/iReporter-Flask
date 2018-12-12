from datetime import datetime
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from app.database_config import init_db


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class UsersModel():
    """ Docstring for my users model """

    def __init__(self):
        self.db = init_db()
        self.registered = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.isAdmin = "isAdmin"

    """ save our users and appendthem to the database """
    def save(self, firstname, lastname, othernames, username, email,
             phonenumber, password):

        userdata = {
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
        curr = self.db.cursor()
        curr.execute(inquire, userdata)
        self.db.commit()
        return userdata

    """get all the users """
    def get_users(self):

        user_conn = self.db
        curr = user_conn.cursor()
        curr.execute("""SELECT user_id, firstname, lastname,
                     othernames, username, email, phonenumber, registered,
                     isAdmin, password FROM users""")
        user_info = curr.fetchall()
        response = []

        for key, userrecords in enumerate(user_info):
            user_id, firstname, lastname, othernames, username, email,
            phonenumber, registered, isAdmin, password = userrecords
            userdata = dict(
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
            response.append(userdata)
        return response

    """ get one user's data"""
    def get_user_id(self, id):
        """ Get a user by ID """
        user_conn = self.db
        curr = user_conn.cursor()
        curr.execute("""SELECT * FROM users WHERE user_id=%s""", (id, ))

        selectuser = curr.fetchone()

        user_conn.commit()

        if selectuser:
            return selectuser

    def delete_user(self, user_id):
        user_conn = self.db
        curr = user_conn.cursor()
        curr.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        user_conn.commit()

    def get_username_user(self, username):
        """ Get user by username """
        user_conn = self.db
        curr = user_conn.cursor()
        curr.execute("""SELECT * FROM users WHERE username=%s""", (username, ))
        selectuser = curr.fetchone()
        user_conn.commit()
        if selectuser:
            return selectuser

    def login_user(self):
        user_conn = self.db
        curr = user_conn.cursor()
        username = request.get_json()['username']
        curr.execute("SELECT * FROM users WHERE username='" + str(username) + "'")
        user_conn.commit
