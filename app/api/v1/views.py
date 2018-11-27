from flask import jsonify, make_response, request
from flask_restful import Resource, Api, reqparse

from .models import IncidentsModel


class MyIncidents(Resource, IncidentsModel):
    """ Docstring for my records"""

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
            "Red flag record created": resp
        }), 201)

    def get(self):
        resp = self.db.get_incidents()
        return make_response(jsonify({
            "my list of records": resp
        }), 200)
