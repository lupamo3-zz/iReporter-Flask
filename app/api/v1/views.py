from flask import jsonify, make_response, request
from flask_restful import Resource, Api, abort, request

from .models import IncidentsModel, incidents_list


class MyIncidents(Resource, IncidentsModel):
    """ Docstring for MyIncidents class, Myincidents class has methods for 
    users to Create redflags(POST) and to get all red flag records(GET)"""

    def __init__(self):
        self.db = IncidentsModel()

    def post(self):
        """ Create a redflag """
        data = request.get_json(force=True)
        createdBy = data['createdBy']
        location = data['location']
        comment = data['comment']

        resp = self.db.save(createdBy, location, comment)

        if resp == "missing data":

            return make_response(jsonify({
                "status": 400,
                "error": "Red-flag Creation not succesful"
            }))

        return make_response(jsonify({
            "status": 201,
            "data": [{
                "id": 1,
                "record": resp,
                "message": "Created redflag record"
            }]
        }), 201)

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
            "error": "Red-flag not found"
        }))


class MyRecords(Resource, IncidentsModel):
    """ Docstring for MyRecords class, this class has methods that allows
    users to get specific records(GET by id), make changes to a
    record(PATCH) and to delete sepecific records(DELETE by id)"""

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
                }), 200)

        return make_response(
            jsonify(
                {
                    "status": 404,
                    "error": "Redflag with that id not found"
                }
            )
        )

    def delete(self, id):
        """ Allows you to delete a red-flag record """
        incidel = self.db.get_incidents()
        deleting = self.db.get_one(id)

        if not deleting:
            return {'message': 'Redflag not found'}, 404
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
            return {'message': 'Redflag to be edited not found'}, 200
        else:
            topatch.update(request.get_json())

        return make_response(jsonify({
            'status': 200,
            'data': [{
                'id': 200,
                "data": topatch,
                "message": "Updated red-flag record location"
            }]
        }), 201)
