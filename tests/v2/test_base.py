import os
import unittest
import json
import pytest

from app import create_app
from app.database_config import test_init_db


class BaseTestClass(unittest.TestCase):
    """ This is the base class has test data """

    def setUp(self):
        """ Defines the test data """

        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.db = test_init_db()

        self.data = {
            "comment": "I am doing it",
            "createdBy": 1,
            "createdOn": "2018-12-12 15:45:07",
            "images": "images",
            "location": "naironi",
            "status": "Draft",
            "type": "Redflags",
            "videos": "videos"
        }

        self.no_input = {
        }

        self.auth_signup = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "R",
            "username": "Andela",
            "email": "andela@andela.Kenya",
            "phonenumber": "0724716026",
            "password": "Eatlivecode"
        }

        self.no_comment = {
            "createdOn": "2018-11-29 05:21:37",
            "createdBy": "Norbert",
            "location": "Mount Sinai",
            "status": "There is a bush on fire",
            "comment": "",
            "id": 1
        }

        self.token_login = {
            "username": "Andela",
            "password": "Eatlivecode"
        }

        self.auth = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "R",
            "username": "Andela1",
            "email": "andela@andela.andela",
            "phonenumber": "0717245777",
            "password": "Eatlivecode"
        }
        self.login = {
            "username": "Andela1",
            "password": "Eatlivecode"
        }
        self.invalid = {
            "username": "Andela1",
            "password": "Eatlivecod"
        }
        self.unregistered = {
            'username': 'ramsaybolton',
            'password': 'dark'
        }
        self.duplicate = {
            "firstname": "Anjichi",
            "lastname": "Lupamo",
            "othernames": "R",
            "username": "Andela1",
            "email": "andela@andela.andela",
            "phonenumber": "0717245777",
            "password": "Eatlivecode"
        }

        res = self.client.post(
            '/api/v2/signup',
            data=json.dumps(self.auth_signup),
            headers={"content-type": "application/json"}
        )
        login_res = self.client.post(
            '/api/v2/login',
            data=json.dumps(self.token_login),
            headers={"content-type": "application/json"}
        )
        response = json.loads(login_res.data)
        print(response)
        self.auth_token = response["access_token"]

    def tearDown(self):

        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""DROP TABLE IF EXISTS users CASCADE """)
        curr.execute("""DROP TABLE IF EXISTS incidents CASCADE """)
        dbconn.commit()


if __name__ == "__main__":
    unittest.main()
