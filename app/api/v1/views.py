from flask import jsonify, make_response, request
from flask_restful import Resource, Api, abort, request

from .models import IncidentsModel


class MyIncidents(Resource, IncidentsModel):
    """ Docstring for MyIncidents"""

    def __init__(self):
        self.db = IncidentsModel()

    def post(self):
        """ Create a redflag """
        data = request.get_json(force=True)
        createdOn = data['createdOn'],
        createdBy = data['createdBy'],
        location = data['location'],
        status = data['status'],
        comment = data['comment'],

        resp = self.db.save(createdOn, createdBy, location, status,
                            comment)

        if resp:

            return make_response(jsonify({
                "status": 201,
                "data": [{
                    "id": 1,
                    "message": "Created redflag record"
                }]
            }), 201)

        else:

            return make_response(jsonify({
                "status": 400,
                "error": "Red-flag Creation not succesful"
            }))

    def get(self):
        """ Get all red flag records """
        fetch_all = self.db.get_incidents()

        if fetch_all:

            return make_response(jsonify({
                "status": 200,
                "data": fetch_all
            }), 200)

        else:
            return make_response(jsonify({
                "status": 404,
                "error": "Red-flag not found"
            }))


class MyRecords(Resource, IncidentsModel):
    """ Docstring for MyRecords"""

    def __init__(self):
        self.db = IncidentsModel()

    def get(self, id):
        """ Get a specific red-flag record """
        incidents = self.db.get_incidents()
        for i in incidents:
            if i['id'] == id:

                return make_response(jsonify({
                    "status": 200,
                    "data": i
                }),
                    200)
            else:
                return make_response(
                    jsonify(
                        {
                            "status": 404,
                            "error": "Redflag Not found"
                        }
                    )
                )

    def delete(self, id):
        """ Allows you to delete a red-flag record """
        incidel = self.db.get_incidents()
        deleting = self.db.get_one(id)

        if not deleting:
            return {'message': 'not found'}, 404
        else:
            incidel.remove(deleting)

        return make_response(jsonify({
            'status': 200,
            "data": [{
                "id": 1,
                "message": "red-flag record has been deleted"
            }]
        }))

    def patch(self, id):
        """ Allows you to make changes to an exisiting red-flag """
        topatch = self.db.get_one(id)

        if not topatch:
            return {'message': 'not found'}, 404
        else:
            topatch.update(request.get_json())

        return make_response(jsonify({
            'status': 200,
            'data': [{
                'id': 200,
                "message": "Updated red-flag record's location"
            }]
        }), 201)
