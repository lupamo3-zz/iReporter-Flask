from datetime import datetime
from flask import request


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

incidents_list = []


class IncidentsModel():
    """ Docstring for my incidents model """

    def __init__(self):
        self.db = incidents_list
        self.status = "Draft"
        self.time = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    """ save our data and appends it to a list """
    def save(self, createdBy, location, comment):
        incidentdata = {
            "id": self.userid(),
            "createdBy": createdBy,
            "location": location,
            "comment": comment,
            "status": self.status,
            "time": self.time
        }
        validate_data = "missing data"

        for i in incidentdata:
            if type(createdBy) != str or type(location) != str or type(comment) != str:
                return validate_data
        self.db.append(incidentdata)
        return incidentdata

    """get all the incidents """
    def get_incidents(self):
        return self.db

    """ get one incident data"""
    def get_one(self, id):
        result = None

        for instance in self.db:
            if instance['id'] == id:
                result = instance
        return result

    def userid(self):
        if len(self.db):
            return self.db[-1]["id"] + 1
        return 1
