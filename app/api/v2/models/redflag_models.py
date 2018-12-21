from datetime import datetime
import psycopg2
from app.database_config import init_db
from app.api.v2.models.user_models import UsersModel
from app.api.v2.views.authentication import SignIn


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class IncidentsModel():
    """ Docstring for my incidents model """

    def __init__(self):
        self.db = init_db()
        self.status = "Draft"
        self.createdOn = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

    """ save our data and appends to the database """

    def save(self, comment, location, images, videos, createdBy, incidentType):

        incident_data = {
            "comment": comment,
            "createdBy": createdBy,
            "createdOn": self.createdOn,
            "images": images,
            "location": location,
            "status": self.status,
            "incidentType": incidentType,
            "videos": videos
        }

        query = """INSERT INTO incidents (location, comment, createdBy,
                 status, createdOn, images, videos, incidentType) VALUES (
                  %(location)s, %(comment)s, %(createdBy)s, %(status)s,
                   %(createdOn)s, %(images)s, %(videos)s, %(incidentType)s)"""

        currsor = self.db.cursor()
        currsor.execute(query, incident_data)
        self.db.commit()
        return incident_data

    """get all the incidents """

    def get_incidents(self):

        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute("""SELECT incidents_id, incidentType, status, comment,
                    createdBy, createdOn, location,  images, videos
                    FROM incidents""")
        data = currsor.fetchall()
        response = []

        for key, records in enumerate(data):
            incidents_id, incidentType, status, comment, createdBy, createdOn, location, images, videos = records
            datar = dict(
                incidents_id=int(incidents_id),
                incidentType=incidentType,
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
        currsor.execute(f"DELETE FROM incidents WHERE incidents_id = {id};")
        db_connection.commit()
        return "Incident record has been deleted"

    def edit_redflags(self, incidents_id, createdBy):
        """ Query to edit redflag details """
        query = """ UPDATE incidents
                SET createdBy = %s
                WHERE incidents_id = %s"""
        db_connection = self.db
        currsor = db_connection.cursor()
        if UsersModel().check_if_admin():
            currsor.execute(query, (createdBy, incidents_id))
        else:
            currsor.execute(query, (createdBy, incidents_id))
        db_connection.commit()

    def get_incident_by_id(self, id):
        """ Get redflag or interevention details by id"""
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(f"SELECT * FROM incidents WHERE incidents_id = {id};")
        incident = currsor.fetchall()
        response = []

        for key, records in enumerate(incident):
            incidents_id, incidentType, status, comment, createdBy, createdOn, location, images, videos = records
            datar = dict(
                incidents_id=int(incidents_id),
                incidentType=incidentType,
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

    def check_existing_comment(self, comment):
        """ To check comment isn't the same """
        user_connection = self.db
        currsor = user_connection.cursor()
        currsor.execute("""SELECT * FROM users WHERE comment=%s""", (comment, ))
        comment = currsor.fetchone()
        user_connection.commit()
        if comment:
            return True
        False

    def update_status(self, status, incidents_id):
        """ Query for admin to update status details """
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(
            """ UPDATE Incidents
            SET status = %s
            WHERE incidents_id=%s""", (status, incidents_id)
        )
        db_connection.commit()

    def get_user_role(self, current_user):
        """ Check if admin or not """
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(
            """SELECT * FROM Users WHERE username = %s;""", (current_user,)
        )
        admin_status = currsor.fetchall()[0][8]

        return admin_status

    def get_created_by(self, current_user):
        """ Get who created """
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(
            """SELECT * FROM Users WHERE username = %s;""", (current_user,)
        )
        created_by = currsor.fetchall()[0][4]

        return created_by

    def get_email_update(self, id):
        """ Get email after a certain update """
        db_connection = self.db
        currsor = db_connection.cursor()
        currsor.execute(
            """SELECT createdBy FROM Incidents WHERE incidents_id = %s;""", (id,)
        )
        data = currsor.fetchone()