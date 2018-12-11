import os 
import unittest
import json 
import pytest

from ... import create_app
from ...database_config import test_init_db


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


    def test_user_signup(self):
        """Test to see user signing up"""
        res = self.client.post(
            '/signup', 
            data=json.dumps(self.auth),
            content_type="application/json"
        )
        self.assertEqual(res.status_code,  201)


    def test_user_login(self):
        """ Test that registered users can login """
        res = self.client.post(
            '/signup',
            data=self.auth
        )
        self.assertEqual(res.status_code, 201)
        login_res = self.client.post(
            '/login',
            data=self.auth
        )
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_user_registered(self):
        """ CHeck if users are already registered """
        res = self.client.post(
            '/signup',
            data=self.auth
        )
        self.assertEqual(res.status_code, 201)
        second_res = res = self.client.post(
            '/signup',
            data=self.auth
        )
        self.assertEqual(second_res.status_code, 202)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result['message'], "User already exists, please login.")

    def test_unregistered_login(self):
        """ Check what happens when unregistered user tries to login """
        unregistered = {
            'username': 'ramsaybolton',
            'password': 'dark'
        }
        res = self.client.post(
            '/signup',
            data=unregistered
        )
        result = json.loads(res.data.decode())

        self.assertEqual(res.status_code, 401)
        self.assertEqual(result['message'], "Wrong credentials" )
        

    def tearDown(self):
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("DROP TABLE users")
        dbconn.commit()


if __name__ == "__main__":
    unittest.main()
