from flask import jsonify, make_response, request
from flask_restful import Resource, Api, abort, request
from flask_jwt_extended import jwt_required, jwt_refresh_token_required

from ..models.redflag_models import IncidentsModel
from ....database_config import init_db


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
            return make_response(jsonify({
                "status": 200,
                "message": "No data input"
            }), 404)
        elif not data['location'] or not data["comment"]:
            return make_response(jsonify({
                "status": 404,
                "data": [{"message": "Ensure you have\
 filled all fields. i.e {} " .format(data)}]
            }), 404)
            
        return make_response(jsonify({
            "status": 201,
            "data": [{
                "incident_created": data,
                "message": "Created redflag record"
            }]
        }), 201)

    @jwt_required
    def get(self):
        """ Get all red flag records """
        fetch_all = self.db.get_incidents()

        if fetch_all:

            return make_response(jsonify({
                "status": 200,
                "data": fetch_all
            }), 200)

        return make_response(jsonify({
            "status": 404,
            "error": "No Red-flag found"
        }))


class MyRecords(Resource, IncidentsModel):
    """ Docstring for MyRecords class, this class has methods that allows
    users to get specific records(GET by id), make changes to a
    record(PATCH) and to delete sepecific records(DELETE by id)"""

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def get(self, id):
        """ Get a specific red-flag record """
        incidents = self.db.get_incidents()
        for i in incidents:
            if i['incidents_id'] == id:

                return make_response(jsonify({
                    "status": 200,
                    "data": i
                }), 200)

        return make_response(
            jsonify(
                {
                    "status": 404,
                    "error": "Redflag with that id not found"
                }
            ), 404
        )

    @jwt_required
    def delete(self, id):
        """ Allows you to delete a red-flag record """
        deleting = self.db.delete_redflag(id)

        if deleting:
            return make_response(jsonify({
                'status': 200,
                "data": [{
                    "id": id,
                    "message": "red-flag record has been deleted"
                }]
            }))
        return make_response(jsonify({
            'status': 200,
            "data": [{
                "id": id,
                'message': 'Redflag not found'
            }]
        }), 404)


class MySpecificRecords(Resource, IncidentsModel): 
    """ Users can change the location of a record occurrence using Patch """

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def patch(self, id):
        """ Makes the location editable by user """
        gett = self.db.get_incident_by_id(id=id)
        data = request.get_json(force=True)
        print(gett)
        if gett:
            self.db.update_location(data['location'], id)
            return make_response(jsonify({
                "New Location": data['location'],
                "message": "Updated location successfully",
                "status": 200
            }))
        return make_response(jsonify({
            "message": " Incident not found",
            "status": 404
        }), 404)
 
class MyCommentRecords(Resource, IncidentsModel):
    """ Edit the comment of a specific intervention record. """

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def patch(self, id):
        """ Allows you to make changes to redflag commments"""
        gett = self.db.get_incident_by_id(id=id)
        data = request.get_json(force=True)
        print(gett)
        if gett:
            self.db.update_comment(data['comment'], id)
            return make_response(jsonify({
                "New Comment": data['comment'],
                "message": "Updated comment successfully",
                "status": 200
            }))
        return make_response(jsonify({
            "message": " Incident not found",
            "status": 404
        }), 404)