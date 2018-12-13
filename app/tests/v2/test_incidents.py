import os
import unittest
import json
import pytest

from app import create_app
from app.database_config import test_init_db


class TestRedflags(unittest.TestCase):
    """This class represents the test redflag case """

    def setUp(self):
        """Defines the test variables """

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
        self.auth_token = response["access_token"]

    def test_get_all_records(self):
        """ Test if API endpoint is able to get all records correctly """
        response = self.client.get(
            '/api/v2/incidents',
            # data=self.data,
            headers={'authorization': 'Bearer ' + self.auth_token})
        self.assertEqual(response.status_code, 200)

    def test_creation_of_records(self):
        """ Test if API endpoint can create a redflag (POST)"""
        response = self.client.post(
            '/api/v2/incidents',
            data=json.dumps(self.data),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer '+self.auth_token}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Created redflag record', str(response.data))

    def test_get_one_record(self):
        """ Test if API is able to get a single ID record"""
        response = self.client.post(
            '/api/v2/incidents',
            data=json.dumps(self.data),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer ' + self.auth_token}
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.get(
            "/api/v2/incidents/2",
            headers={'Authorization': 'Bearer ' + self.auth_token})
        self.assertEqual(response.status_code, 200)

    def test_records_deletion(self):
        """Test if API can delete existing records """
        rv = self.client.post(
            '/api/v2/incidents',
            data=json.dumps(self.data),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer ' + self.auth_token}
        )
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete(
            '/api/v2/incidents/1',
            headers={'Authorization': 'Bearer ' + self.auth_token})
        self.assertEqual(res.status_code, 200)

    def test_record_without_comment(self):
        """ Test if API can post with one field not filled"""
        response = self.client.post(
            '/api/v2/incidents',
            data=json.dumps(self.no_comment),
            headers={"content-type": "application/json",
                     'authorization': 'Bearer ' + self.auth_token}
        )
        self.assertEqual(response.status_code, 404)

    def test_creation_record_empty_fileds(self):
        """ Test if API can post with all fields empty"""
        response = self.client.post(
            '/api/v2/incidents',
            data=json.dumps(self.no_input),
            headers={"content-type": "application/json",
                     'authorization': 'Bearer ' + self.auth_token}
        )
        self.assertEqual(response.status_code, 404)

    def test_no_record_to_delete(self):
        """Test if API can delete existing records """
        rv = self.client.post(
            '/api/v2/incidents',
            data=json.dumps(self.data),
            headers={"content-type": "application/json",
                     'authorization': 'Bearer ' + self.auth_token}
        )
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete(
            '/api/v2/incidents/20',
            headers={'authorization': 'Bearer ' + self.auth_token})
        self.assertEqual(res.status_code, 200)

    def test_none_existent_record(self):
        """ Test if API is able to get non-existent record"""
        response = self.client.get(
            '/api/v2/incidents/200',
            headers={'Authorization': 'Bearer ' + self.auth_token}
        )
        self.assertEqual(response.status_code, 404)

    def test_editing_location(self):
        """ Test if API is able to change location """
        response = self.client.post(
            'api/v2/incidents',
            data=json.dumps(self.data),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer ' + self.auth_token}
        )
        patch_record = {
            'location': 'Andela Uganda'
        }
        response = self.client.patch(
            "/api/v2/incidents/2/location",
            data=json.dumps(patch_record),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer ' + self.auth_token})
        data = json.loads(response.data)
        self.assertEqual(data["New Location"], "Andela Uganda")

    def tearDown(self):
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("DROP TABLE IF EXISTS incidents CASCADE")
        dbconn.commit()


if __name__ == '__main__':
    unittest.main()
