from flask import jsonify, make_response, request
from flask_restful import Resource, Api, abort, request

from .models import IncidentsModel


class MyIncidents(Resource, IncidentsModel):
    """ Docstring for MyIncidents"""

    def __init__(self):
        self.db = IncidentsModel()

    def post(self):
        data = request.get_json()
        createdBy = data['createdBy']
        createdOn = data['createdOn']
        location = data['location']
        status = data['status']
        comment = data['comment']

        resp = self.db.save(createdBy, createdOn, location, status,
                            comment)

        return make_response(jsonify({
            "status": 201,
            "data": [{
                "id": 1,
                "message": "Created redflag record"
            }]
        }), 201)

    def get(self):
        resp = self.db.get_incidents()
        return make_response(jsonify({
            "status": 200,
            "data": resp
        }), 200)


class MyRecords(Resource, IncidentsModel):
    """ Docstring for MyRecords"""

    def __init__(self):
        self.db = IncidentsModel()

    def get(self, id):
        incidents = self.db.get_incidents()
        for i in incidents:
            if i['id'] == id:
                print(id)
                return make_response(jsonify({
                    "status": 200,
                    "data": i
                }), 200)

    

    def patch(self, id):
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
