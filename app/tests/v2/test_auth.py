import os
import unittest
import json
import pytest

from app import create_app
from app.database_config import test_init_db


class TestAuthorization(unittest.TestCase):
    """ Test for the user authentication """

    def setUp(self):
        """Defines the test variables. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.db = test_init_db()

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

    def test_user_signup(self):
        """Test to see user signing up"""
        res = self.client.post(
            '/api/v2/signup',
            data=json.dumps(self.auth),
            headers={"content-type": "application/json"}
        )
        return res

    def test_user_registration(self):
        """Test post success"""
        response = self.test_user_signup()
        self.assertEqual(response.status_code,  201)

    def test_user_login(self):
        """ Test that registered users can login """
        self.test_user_signup()
        login_res = self.client.post(
            '/api/v2/login',
            data=json.dumps(self.login),
            headers={"content-type": "application/json"}
        )
        result = json.loads(login_res.data.decode())
        self.assertEqual(login_res.status_code, 200)

    def test_existing_username(self):
        """ CHeck if users are already registered """
        self.test_user_signup()
        second_res = res = self.client.post(
            '/api/v2/signup',
            data=json.dumps(self.duplicate),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(second_res.status_code, 400)
        result = json.loads(second_res.data.decode())

    def test_unregistered_username(self):
        """ Check what happens when unregistered user tries to login """
        res = self.client.post(
            '/api/v2/login',
            data=json.dumps(self.unregistered),
            headers={"content-type": "application/json"}
        )
        result = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 401)

    def test_incorrect_login_details(self):
        """ Check user attempts to login with incorrect details """
        res = self.client.post(
            '/api/v2/login',
            data=json.dumps(self.invalid),
            headers={"content-type": "application/json"}
        )
        result = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 401)

    def tearDown(self):

        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("DROP TABLE IF EXISTS users CASCADE ")
        dbconn.commit()


if __name__ == "__main__":
    unittest.main()
