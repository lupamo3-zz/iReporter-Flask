import os
import json
import pytest

from tests.v2.test_base import BaseTestClass


class TestAuthorization(BaseTestClass):
    """ Test for the user authentication """

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
        result = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["message"], "User Andela1 created, now login ")

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
        self.assertEqual(result["data"], "Logged in as Andela1")

    def test_existing_username(self):
        """ Check if users are already registered """
        self.test_user_signup()
        second_res = self.client.post(
            '/api/v2/signup',
            data=json.dumps(self.duplicate),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(second_res.status_code, 400)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result["message"], "User Andela1 already exists")

    def test_unregistered_username(self):
        """ Check what happens when unregistered user tries to login """
        res = self.client.post(
            '/api/v2/login',
            data=json.dumps(self.unregistered),
            headers={"content-type": "application/json"}
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result["Message"],
            'User ramsaybolton doesn\'t exist, Kindly register')

    def test_incorrect_login_details(self):
        """ Check user attempts to login with incorrect details """
        res = self.client.post(
            '/api/v2/login',
            data=json.dumps(self.invalid),
            headers={"content-type": "application/json"}
        )
        result = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)


if __name__ == "__main__":
    unittest.main()