from datetime import datetime
from flask import request

from ...database_config import init_db


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
    def save(self, comment, location, images, videos):

        incidentdata = {
            "incidents_id": self.incidents_id,
            "location": location,
            "comment": comment,
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

        query = """INSERT INTO incidents (location, comment,
                 status, createdOn, images, videos, type) VALUES (
                  %(location)s, %(comment)s, %(status)s, %(createdOn)s,
                  %(images)s, %(videos)s, %(type)s)"""
        curr = self.db.cursor()
        curr.execute(query, incidentdata)
        self.db.commit()
        return incidentdata

    """get all the incidents """
    def get_incidents(self):

        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT incidents_id, type, status, comment, createdOn, 
                    location,  images, videos FROM incidents""")
        data = curr.fetchall()
        resp = []

        for r, records in enumerate(data):
            incidents_id, type, status, comment, createdOn, location, images, videos = records
            datar = dict(
                incidents_id=int(incidents_id),
                type=type,
                status=status,
                comment=comment,
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

    def patch_redflags(self, location, comment, videos, images):
        patchdata = {
            "location": location,
            "comment": comment,
            "images": images,
            "videos": videos,
        }

        query = """INSERT INTO incidents (location, comment,
                 images, videos) VALUES (
                  %(location)s, %(comment)s,%(images)s, %(videos)s)"""
        curr = self.db.cursor()
        curr.execute(query, patchdata)
        self.db.commit()
        return patchdata

        for key in patchdata.keys():
            if patchdata[key]:
                columns = ["location", "comment", "images", "videos"]
                for c in columns:
                    curr = self.db.cursor()
                    curr.execute("""UPDATE incidents SET {0} = '{1}' WHERE incidents_id = '{2}'""".format)
