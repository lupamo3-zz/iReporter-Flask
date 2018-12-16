from flask import jsonify, make_response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v2.models.redflag_models import IncidentsModel
from app.api.v2.models.user_models import UsersModel

UsersModel = UsersModel()


class MyIncidents(Resource, IncidentsModel):
    """ Docstring for MyIncidents class, Myincidents class has methods
     for users to Create redflags(POST) and to get all red flag records(GET)"""

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def post(self):
        """ Create a redflag """
        data = request.get_json(force=True)
        try:
            if not data:
                return {"message": "Kindly input user info"}, 200
            elif not data['images'] or not data['comment']:
                return {"message":
                        "Ensure you've filled all field. i.e {}".format(data)}, 400
            elif not data['createdBy'] or not data['videos']:
                return {"message":
                        "Ensure you've filled all field. i.e {}".format(data)}, 400
            elif not data['incidentType'] or not data['location']:
                return {"message":
                        "Ensure you've filled all field. i.e {}".format(data)}, 400
        except:
            return {"KeyError": "Kindly check for missing fields"}, 404

        if len(data['comment'].strip()) < 9:
                return {"error": "comment must be more than 9 characters"}
        elif len(data['location'].strip()) < 2:
                return {"error" "location must be more than 2 characters"}

        comment = data['comment']
        location = data['location']
        images = data['images']
        videos = data['videos']
        createdBy = data['createdBy']
        incidentType = data['incidentType']

        incid_data = self.db.save(
            comment, location, images, videos, createdBy, incidentType
            )
        
        return {"incident_created": incid_data,
                "message": "Created redflag record"}, 201

    @jwt_required
    def get(self):
        """ Get all red flag records """
        fetch_all = self.db.get_incidents()

        if fetch_all:

            return make_response(jsonify({
                "data": fetch_all
            }), 200)

        return {"error": "No Incident found"}, 404


class MyRecords(Resource, IncidentsModel):
    """ Docstring for MyRecords class, this class has methods that allows
    users to get specific records(GET by id), make changes to a
    record(PATCH) and to delete sepecific records(DELETE by id)"""

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def get(self, id):
        """ Get a specific red-flag record """
        current_user = get_jwt_identity()
        if current_user:
            incidents = self.db.get_incident_by_id(id)
            if incidents:

                    return make_response(jsonify({
                        "data": incidents
                    }), 200)

            return {"error": "Incident with that id not found"}, 404
        return {"error": "You aren't authorized to access this route"}, 403

    @jwt_required
    def delete(self, id):
        """ Allows you to delete a red-flag record """
        incidents = self.db.get_incident_by_id(id)
        if not incidents:
            return {"error": "Incident with that id not found"}, 404
        current_user = get_jwt_identity()
        print(current_user)
        deleting = self.db.delete_redflag(id)

        if deleting:
            return {"id": id, "message": deleting}, 200


class MySpecificRecords(Resource, IncidentsModel):
    """ Users can change the location of a record occurrence using Patch """

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def patch(self, id):
        """ Makes the location editable by user """
        get_by_id = self.db.get_incident_by_id(id=id)
        data = request.get_json(force=True)

        if get_by_id:
            self.db.update_location(data['location'], id)
            return {
                "New Location": data['location'],
                "message": "Updated location successfully",
            }, 200
        return {"message": " Incident not found"}, 404


class MyCommentRecords(Resource, IncidentsModel):
    """ Edit the comment of a specific intervention record. """

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def patch(self, id):
        """ Allows you to make changes to redflag commments"""
        data = request.get_json(force=True)
        comment = data['comment']
        check_comment = self.db.check_existing_comment(comment)
        if check_comment:
            return {"Message": "Comment already exists"}
        get_by_id = self.db.get_incident_by_id(id=id)

        if get_by_id:
            self.db.update_comment(data['comment'], id)
            return {"New Comment": data['comment'],
                    "message": "Updated comment successfully"}, 200
        return {"message": " Incident not found"}, 404


class MyStatusRecords(Resource, IncidentsModel):
    """ Edit the comment of a specific intervention record. """

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def patch(self, id):
        """ Admin makes changes to status"""
        fetch_by_id = self.db.get_incident_by_id(id=id)
        data = request.get_json(force=True)
        if data['status'] != 'draft':
            return {
                "message": "Forbidden, status can only be updated when draft"
            }, 403
        elif fetch_by_id:
            self.db.update_status(data['status'], id)
            return {"New status": data['status'],
                    "message": "Updated status successfully"}, 200
        return {"message": " Status Incident not found"}, 404
