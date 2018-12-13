from flask import jsonify, make_response
from flask_restful import Resource, request
from flask_jwt_extended import jwt_required

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
            return {"data": {"message": "No data input!"}}, 200
        elif not data['location'] or not data["comment"]:
            return {"data": {"message": "Ensure you have\
 filled all fields. i.e {} " .format(data)}}, 404

        comment = data['comment']
        location = data['location']
        images = data['images']
        videos = data['videos']
        createdBy = data['createdBy']

        incid_data = self.db.save(comment, location, images, videos, createdBy)
        return {"data": [{"incident_created": incid_data,
                          "message": "Created redflag record"}]}, 201

    @jwt_required
    def get(self):
        """ Get all red flag records """
        fetch_all = self.db.get_incidents()

        if fetch_all:

            return make_response(jsonify({
                "data": fetch_all
            }), 200)

        return {"error": ["No Incidence found"]}, 404


class MyRecords(Resource, IncidentsModel):
    """ Docstring for MyRecords class, this class has methods that allows
    users to get specific records(GET by id), make changes to a
    record(PATCH) and to delete sepecific records(DELETE by id)"""

    def __init__(self):
        self.db = IncidentsModel()

    @jwt_required
    def get(self, id):
        """ Get a specific red-flag record """
        incidents = self.db.get_incident_by_id(id)
        if incidents:

                return make_response(jsonify({
                    "data": incidents
                }), 200)

        return {"error": ["Incident with that id not found"]}, 404
          
    # @jwt_required
    # def delete(self, id):
    #     """ Allows you to delete a red-flag record """
    #     deleting = self.db.delete_redflag(id)

    #     if deleting:
    #         return make_response(jsonify({
    #             'status': 200,
    #             "data": [{
    #                 "id": id,
    #                 "message": "red-flag record has been deleted"
    #             }]
    #         }))
    #     return make_response(jsonify({
    #         'status': 200,
    #         "data": [{
    #             "id": id,
    #             'message': 'Redflag not found'
    #         }]
    #     }), 404)


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
            return {"data": [{
                "New Location": data['location'],
                "message": "Updated location successfully",
            }]}, 200
        return {"data": [{"message": " Incident not found"}]}, 404


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
            return {"data": [{"New Comment": data['comment'],
                              "message": "Updated comment successfully"}]}, 200
        return {"data": [{"message": " Incident not found"}]}, 404
