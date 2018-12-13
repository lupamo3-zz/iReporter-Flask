from datetime import datetime

from app.database_config import init_db


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class IncidentsModel():
    """ Docstring for my incidents model """

    def __init__(self):
        self.db = init_db()
        self.status = "Draft"
        self.createdOn = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.type = "Redflags"

    """ save our data and appends to the database """

    def save(self, comment, location, images, videos, createdBy):

        incidentdata = {
            "comment": comment,
            "createdBy": createdBy,
            "createdOn": self.createdOn,
            "images": images,
            "location": location,
            "status": self.status,
            "type": self.type,
            "videos": videos
        }

        query = """INSERT INTO incidents (location, comment, createdBy,
                 status, createdOn, images, videos, type) VALUES (
                  %(location)s, %(comment)s, %(createdBy)s, %(status)s,
                   %(createdOn)s, %(images)s, %(videos)s, %(type)s)"""
        curr = self.db.cursor()
        curr.execute(query, incidentdata)
        self.db.commit()
        return incidentdata

    """get all the incidents """

    def get_incidents(self):

        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT incidents_id, type, status, comment,
                 createdBy, createdOn, location,  images, videos
                  FROM incidents""")
        data = curr.fetchall()
        resp = []

        for key, records in enumerate(data):
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

    def delete_redflag(self, id):
        """ To delete redflag and incident details """
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("DELETE FROM incidents WHERE incidents_id = %s", (id,))
        dbconn.commit()

    def edit_redflags(self, incidents_id, createdBy):
        """ Query to edit redflag details """
        sql = """ UPDATE incidents
                SET createdBy = %s
                WHERE incidents_id = %s"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute(sql, (createdBy, incidents_id))
        dbconn.commit()

    def get_incident_by_id(self, id):
        """ Get redflag or interevention details by id"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute(f"SELECT * FROM incidents WHERE incidents_id = {id};")
        incident = curr.fetchall()
        return incident

    def update_location(self, location, incidents_id):
        """ Query to update user location details """
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute(
            """ UPDATE Incidents
            SET location = %s
            WHERE incidents_id=%s""", (location, incidents_id)
        )
        dbconn.commit()

    def update_comment(self, comment, incidents_id):
        """ Query to update user comment details """
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute(
            """ UPDATE Incidents
            SET comment = %s
            WHERE incidents_id=%s""", (comment, incidents_id)
        )
        dbconn.commit()
