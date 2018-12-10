from datetime import datetime
from flask import request

from ....database_config import init_db


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class IncidentsModel():
    """ Docstring for my incidents model """

    def __init__(self):
        self.db = init_db()
        self.status = "Draft"
        self.createdOn = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.type = "Redflags"
        self.incidents_id = "incidents_id"

    """ save our data and appends to the database """
    def save(self, comment, location, images, videos, createdBy):

        incidentdata = {
            "incidents_id": self.incidents_id,
            "location": location,
            "comment": comment,
            "createdBy": createdBy,
            "status": self.status,
            "createdOn": self.createdOn,
            "images": images,
            "videos": videos,
            "type": self.type
        }

        # validate_data = "missing data"

        # for i in incidentdata:
        #     if type(location) != str or type(comment) != str or type(self.status) != str:
        #             return validate_data
        #     elif type(self.incidents_id) != int or type(self.createdOn) != str:
        #         return validate_data

        query = """INSERT INTO incidents (location, comment, createdBy,
                 status, createdOn, images, videos, type) VALUES (
                  %(location)s, %(comment)s, %(createdBy)s, %(status)s, %(createdOn)s,
                  %(images)s, %(videos)s, %(type)s)"""
        curr = self.db.cursor()
        curr.execute(query, incidentdata)
        self.db.commit()
        return incidentdata

    """get all the incidents """
    def get_incidents(self):

        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT incidents_id, type, status, comment, createdBy, createdOn, 
                    location,  images, videos FROM incidents""")
        data = curr.fetchall()
        resp = []

        for r, records in enumerate(data):
            incidents_id, type, status, comment, createdBy, createdOn, location, images, videos = records
            datar = dict(
                incidents_id=int(incidents_id),
                type=type,
                status=status,
                comment=comment,
                createdBy=createdBy,
                createdOn=createdOn,
                location=location,
                images=images,
                videos=videos
            )
            resp.append(datar)
        return resp

    """ get one incident data"""
    def get_one(self, incidents_id):
        result = None

        for instance in self.db:
            if instance['incidents_id'] == id:
                result = instance
        return result

    def delete_redflag(self, id):
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("DELETE FROM incidents WHERE incidents_id = %s", (id,))
        dbconn.commit()

    def edit_redflags(self, incidents_id, createdBy):
        sql = """ UPDATE incidents
                SET createdBy = %s
                WHERE incidents_id = %s"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute(sql, (createdBy, incidents_id))
        dbconn.commit()

    def get_incident_by_id(self, id):
        # Todo
        # Add other things to update
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute(f"SELECT * FROM incidents WHERE incidents_id = {id};")
        incident = curr.fetchall()
        return incident

    def update_location(self, location, incidents_id):
        dbconn = self.db
        curr=dbconn.cursor()
        curr.execute(
            """ UPDATE Incidents
            SET location = %s
            WHERE incidents_id=%s""", (location, incidents_id)
             )
        dbconn.commit()

    def update_comment(self, comment, incidents_id):
        dbconn = self.db
        curr=dbconn.cursor()
        curr.execute(
            """ UPDATE Incidents
            SET comment = %s
            WHERE incidents_id=%s""", (comment, incidents_id)
             )
        dbconn.commit()