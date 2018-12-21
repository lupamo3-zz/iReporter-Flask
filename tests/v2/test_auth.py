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
        self.assertEqual(result["message"], "User testusr created login ")

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
        self.assertEqual(result["data"], "Logged in as testusr")

    def test_existing_username(self):
        """ Check if users are already registered """
        self.test_user_signup()
        second_res = self.client.post(
            '/api/v2/signup',
            data=json.dumps(self.auth),
            headers={"content-type": "application/json"}
        )
        print(second_res.data)
        self.assertEqual(second_res.status_code, 400)
        result = json.loads(second_res.data.decode())
        self.assertEqual(result["message"], "User testusr already exists")

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

    def test_signup_with_exisiting_phonenumber(self):
        """ Check is user attempts to signin with a number 
        that already exists """
        self.test_user_signup()
        res = self.client.post(
            'api/v2/signup',
            data=json.dumps(self.cell),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result["message"],
            "A user with the phonenumber already exists")

    def test_signup_with_exisiting_username(self):
        """ Check is user attempts to signin with a number 
        that already exists """
        self.test_user_signup()
        res = self.client.post(
            'api/v2/signup',
            data=json.dumps(self.username),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result["message"],
            "User testusr already exists")

    def test_signup_with_exisiting_email(self):
        """ Check is user attempts to signin with a number 
        that already exists """
        self.test_user_signup()
        res = self.client.post(
            'api/v2/signup',
            data=json.dumps(self.email),
            headers={"content-type": "application/json"}
        )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertEqual(
            result["message"],
            "A user with the email already exists.")

    def test_signup_with_missingfields(self):
        """ Check if user can signu with missing fields """
        res = self.client.post(
            'api/v2/signup',
            data=json.dumps(self.missing_fields),
            headers={"content-type": "application/json"}
        )
        result = json.loads(res.data.decode())
        self.assertEqual(
            result["KeyError"],
            "Kindly check for missing fields"
        )
        self.assertEqual(res.status_code, 404)

if __name__ == "__main__":
    unittest.main()
