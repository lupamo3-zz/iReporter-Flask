from datetime import datetime
from flask import request

from ....database_config import init_db


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class UsersModel():
    """ Docstring for my users model """

    def __init__(self):
        self.db = init_db()
        self.registered = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.user_id = "user_id"
        self.isAdmin = "isAdmin"

    """ save our users and appendthem to the database """
    def save(self, firstname, lastname, othernames, username, email,
             phonenumber, password, confirm_password):

        userdata = {
            "user_id": self.user_id,
            "firstname": firstname,
            "lastname": lastname,
            "othernames": othernames,
            "username": username,
            "email": email,
            "phonenumber": phonenumber,
            "registered": self.registered,
            "isAdmin": False or True,
            "password": password,
            "confirm_password": confirm_password
        }

        inquire = """INSERT INTO users (firstname, lastname,
                 othernames, username, email, phonenumber, registered,
                  isAdmin, password, confirm_password) VALUES (
                  %(firstname)s, %(lastname)s, %(othernames)s, %(username)s,
                  %(email)s, %(phonenumber)s, %(registered)s, %(isAdmin)s,
                   %(password)s, %(confirm_password)s)"""
        curr = self.db.cursor()
        curr.execute(inquire, userdata)
        self.db.commit()
        return userdata

    """get all the users """
    def get_users(self):

        usconn = self.db
        curr = usconn.cursor()
        curr.execute("""SELECT user_id, firstname, lastname,
                     othernames, username, email, phonenumber, registered,
                     isAdmin, password, confirm_password FROM users""")
        user_info = curr.fetchall()
        response = []

        for i, userrecords in enumerate(user_info):
            user_id, firstname, lastname, othernames, username, email, phonenumber, registered, isAdmin, password, confirm_password = userrecords
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
                password=password,
                confirm_password=confirm_password
            )
            response.append(userdata)
        return response

    """ get one user's data"""
    def get_user_id(self, id):
        """ Get a user by ID """
        usconn = self.db
        curr = usconn.cursor()
        curr.execute("""SELECT * FROM users WHERE user_id=%s""", (id, ))

        selectuser = curr.fetchone()

        usconn.commit()

        if selectuser:
            return selectuser

    def delete_user(self, user_id):
        usconn = self.db
        curr = usconn.cursor()
        curr.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        usconn.commit()
