import os
import json
import pytest

from app.tests.v2.test_base import BaseTestClass


class TestRedflags(BaseTestClass):
    """This class represents the test redflag case """

    def test_get_all_records(self):
        """ Test if API endpoint is able to get all records correctly """
        response = self.client.post(
            '/api/v2/incidents',
            data=json.dumps(self.data),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer ' + self.auth_token}
        )
        response = self.client.get(
            '/api/v2/incidents',
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
            "/api/v2/incidents/1",
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
        self.assertEqual(response.status_code, 400)

    def test_creation_record_empty_fileds(self):
        """ Test if API can post with all fields empty"""
        response = self.client.post(
            '/api/v2/incidents',
            data=json.dumps(self.no_input),
            headers={"content-type": "application/json",
                     'authorization': 'Bearer ' + self.auth_token}
        )
        self.assertEqual(response.status_code, 400)

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
            '/api/v2/incidents/1',
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
            "/api/v2/incidents/1/location",
            data=json.dumps(patch_record),
            headers={"content-type": "application/json",
                     'Authorization': 'Bearer ' + self.auth_token})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
