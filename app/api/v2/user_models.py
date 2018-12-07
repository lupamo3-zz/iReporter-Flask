from datetime import datetime
from flask import request

from ...database_config import init_db


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class UsersModel():
    """ Docstring for my users model """

    def __init__(self):
        self.db = init_db()
        self.registered = datetime.datetime.utcnow()
        self.user_id = "user_id"
        self.isAdmin = "isAdmin"

    """ save our users and appendthem to the database """
    def save(self, firstname, lastname, othernames, username, email,
             phonenumber, registered):

        userdata = {
            "user_id": self.user_id,
            "firstname": firstname,
            "lastname": lastname,
            "othernames": othernames,
            "username": username,
            "email": email,
            "phonenumber": phonenumber,
            "registered": self.registered
        }

        inquire = """INSERT INTO incidents (firstname, lastname,
                 othernames, username, email, phonenumber, registered) VALUES (
                  %(firstname)s, %(lastname)s, %(othernames)s, %(username)s,
                  %(email)s, %(phonenumber)s, %(registered)s)"""
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
                     isAdmin FROM incidents""")
        user_info = curr.fetchall()
        response = []

        for userrecords in enumerate(user_info):
            user_id, firstname, lastname, othernames, username, email, phonenumber, registered, isAdmin = userrecords
            userdata = dict(
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
            response.append(userdata)
        return response

    """ get one user's data"""
    def get_single_user(self, user_id):
        result = None

        for i in self.db:
            if i['user_id'] == id:
                result = i
        return result

    def delete_user(self, id):
        usconn = self.db
        curr = usconn.cursor()
        curr.execute("DELETE FROM users WHERE users_id = %s", (id,))
        usconn.commit()
