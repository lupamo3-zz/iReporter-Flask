from datetime import datetime


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

users_list = []
incidents_list = []


# class UsersModel():
#     """ Docstring for usersmodel"""

#     def __init__(self):
#         self.db = users_list

#     def save(self, firstname, lastname, othernames, email, phoneNumber,
#              username, registered, isAdmin):
#         data = {
#             "id": len(self.db)+1,
#             "firstname": firstname,
#             "lastname": lastname,
#             "othernames": othernames,
#             "email": email,
#             "phoneNumber": phoneNumber,
#             "username": username,
#             "registered": get_timestamp(),
#             "isAdmin": True
#         }

#         self.db.append(data)

#         return self.db

#     def get_users(self):
#         return self.db


class IncidentsModel():
    """ Docstring for my incidents model """

    def __init__(self):
        self.db = incidents_list

    def save(self, createdOn, createdBy, location, status, comment):
        incidentdata = {
            "id": len(self.db)+1,
            "createdOn": get_timestamp(),
            "createdBy": createdBy,
            "location": location,
            "status": status,
            "comment": comment,
        }

        self.db.append(incidentdata)

        return self.db

    def get_incidents(self):
        return self.db
