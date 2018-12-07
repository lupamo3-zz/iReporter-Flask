from flask import jsonify, make_response
from flask_restful import Resource, Api, request

from .user_models import UsersModel


class MyUsers(Resource, UsersModel):
    """ Docstring for MyUsers class, MyUsers class has methods
      to Create Users(POST) and to get all users(GET)"""

    def __init__(self):
        self.db = UsersModel()

    def post(self):
        """ Create a user record """
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

        videos = data['videos']
        comment = data['comment']
        images = data['images']
        location = data['location']

        result = self.db.save(videos, comment, images, location)
        return make_response(jsonify({
            "status": 201,
            "data": [{
                "incident_created": result,
                "message": "Created redflag record"
            }]
        }), 201)

    def get(self):
        """ Get all user records """
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


class MyUsersSpecific(Resource, UsersModel):
    """ Docstring for MyUsersSpecific class, this class has methods that allows
    users to get specific records(GET by id), make changes to a
    record(PATCH) and to delete sepecific records(DELETE by id)"""

    def __init__(self):
        self.db = UsersModel()

    def get(self, id):
        """ Get a specific user record """
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
            )
        )

    def delete(self, id):
        """ Allows you to delete a user  """
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

    def patch(self, id):
        """ Allows you to make changes to an exisiting red-flag """
        topatch = self.db.edit_redflags()

        if not topatch:
            return {'message': 'Redflag to be edited not found'}, 200
        else:
            topatch.update(request.get_json())

        return make_response(jsonify({
            'status': 200,
            'data': [{
                'id': id,
                "data": topatch,
                "message": "Updated red-flag record location"
            }]
        }), 201)
