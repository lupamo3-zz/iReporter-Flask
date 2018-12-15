from flask import jsonify, make_response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.v2.models.redflag_models import IncidentsModel


class MyIncidents(Resource, IncidentsModel):
    """ Docstring for MyIncidents class, Myincidents class has methods
     for users to Create redflags(POST) and to get all red flag records(GET)"""

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def post(self):
        """ Create a redflag """
        data = request.get_json(force=True)
        
        if not data:
            return {"message": "No data input!"}, 400
        elif not data['location'] or not data["comment"]:
            return {"message": "Ensure you have\
 filled all fields. i.e {} " .format(data)}, 400

        comment = data['comment']
        location = data['location']
        images = data['images']
        videos = data['videos']
        createdBy = data['createdBy']
        type = data['type']

        incid_data = self.db.save(
            comment, location, images, videos, createdBy, type
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
        get_by_id = self.db.get_incident_by_id(id=id)
        data = request.get_json(force=True)

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

        if fetch_by_id:
            self.db.update_status(data['status'], id)
            return {"New status": data['status'],
                    "message": "Updated status successfully"}, 200
        return {"message": " Status Incident not found"}, 404
