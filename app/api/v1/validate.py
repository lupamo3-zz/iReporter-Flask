import re
from flask_restful import request
from .models import IncidentsModel


class validate_data():

    def __init__(self):
        self.db = IncidentsModel()

    def check_characters(self):

        data = request.get_json(force=True)

        createdBy = data['createdBy']
        location = data['location']
        comment = data['comment']

        if not re.match('^[a-zA-Z ]+$', createdBy):
            return {'message':
                    "CreatedBy name should be valid alphabetic characters"
                    }, 400

        if not re.match('^[a-zA-Z ]+$', comment):
            return {
                'message':
                "Comment should have valid alphabetic characters"
            }, 400

        if not re.match('^[a-zA-Z ]+$', location):
            return {
                'message':
                "Location name should be of valid alphabetic characters"
            }, 400
