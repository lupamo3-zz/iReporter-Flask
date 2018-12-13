from datetime import datetime

from app.database_config import test_init_db


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class IncidentsModel():
    """ Docstring for my incidents model """

    def __init__(self):
        self.db = test_init_db()
        self.status = "Draft"
        self.createdOn = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.type = "Redflags"

    """ save our data and appends to the database """

    def save(self, comment, location, images, videos, createdBy):

        incident_data = {
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

        currsor = self.db.cursor()
        currsor.execute(query, incident_data)
        self.db.commit()
        return incident_data

    """get all the incidents """

    def get_incidents(self):

        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute("""SELECT incidents_id, type, status, comment,
                 createdBy, createdOn, location,  images, videos
                  FROM incidents""")
        data = currsor.fetchall()
        response = []

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
            response.append(datar)
        return response

    def delete_redflag(self, id):
        """ To delete redflag and incident details """
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute("DELETE FROM incidents WHERE incidents_id = %s", (id,))
        db_connection.commit()
        return "Incident record has been deleted"

    def edit_redflags(self, incidents_id, createdBy):
        """ Query to edit redflag details """
        query = """ UPDATE incidents
                SET createdBy = %s
                WHERE incidents_id = %s"""
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(query, (createdBy, incidents_id))
        db_connection.commit()

    def get_incident_by_id(self, id):
        """ Get redflag or interevention details by id"""
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(f"SELECT * FROM incidents WHERE incidents_id = {id};")
        incident = currsor.fetchall()
        return incident

    def update_location(self, location, incidents_id):
        """ Query to update user location details """
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(
            """ UPDATE Incidents
            SET location = %s
            WHERE incidents_id=%s""", (location, incidents_id)
        )
        db_connection.commit()

    def update_comment(self, comment, incidents_id):
        """ Query to update user comment details """
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(
            """ UPDATE Incidents
            SET comment = %s
            WHERE incidents_id=%s""", (comment, incidents_id)
        )
        db_connection.commit()

    def update_status(self, status, incidents_id):
        """ Query to update user comment details """
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(
            """ UPDATE Incidents
            SET status = %s
            WHERE incidents_id=%s""", (status, incidents_id)
        )
        db_connection.commit()
