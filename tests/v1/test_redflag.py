import os
import unittest
import json
import pytest

from app import create_app


class TestRedflags(unittest.TestCase):
    """This class represents the test redflag case """

    def setUp(self):
        """Defines the test variables """

        self.app = create_app(config_name="development")
        self.client = self.app.test_client()
        self.data = {
            "createdOn": "2018-11-29 05:21:37",
            "createdBy": "Norbert",
            "location": "Mount Sinai",
            "status": "There is a bush on fire",
            "comment": "How hot can it be?",
            "id": 1
        }

        self.no_comment = {
            "createdOn": "2018-11-29 05:21:37",
            "createdBy": "Norbert",
            "location": "Mount Sinai",
            "status": "There is a bush on fire",
            "comment": "",
            "id": 1
        }

        self.no_input = {
        }

    def test_get_all_records(self):
        """ Test if API endpoint is able to get all records correctly """

        response = self.client.get(
            '/api/v1/incidents',
            data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', str(response.data))

    def test_creation_of_records(self):
        """ Test if API endpoint can create a redflag (POST)"""
        response = self.client.post(
            '/api/v1/incidents',
            data=json.dumps(self.data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Created redflag record', str(response.data))

    def test_get_one_record(self):
        """ Test if API is able to get a single ID record"""
        response = self.client.post(
            '/api/v1/incidents',
            data=json.dumps(self.data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/v1/incidents/1")
        self.assertIn("data", str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        """Test if the Patch end point is working """

        response = self.client.post(
            '/api/v1/incidents',
            data=json.dumps(self.data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        patch_record = {
            'location': 'Andela Lagos'
        }
        response = self.client.patch(
            "/api/v1/incidents/1",
            data=json.dumps(patch_record),
            headers={"content-type": "application/json"})
        self.assertIn("Updated red-flag record location",
                      str(response.data))
        self.assertEqual(response.status_code, 200)

    def test_records_deletion(self):
        """Test if API can delete existing records """
        rv = self.client.post(
            '/api/v1/incidents',
            data=json.dumps(self.data),
            content_type="application/json"
        )
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete('/api/v1/incidents/1')
        self.assertEqual(res.status_code, 200)

    def test_record_without_comment(self):
        """ Test if API can post with one field not filled"""
        response = self.client.post(
            '/api/v1/incidents',
            data=json.dumps(self.no_comment),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_creation_record_empty_fileds(self):
        """ Test if API can post with all fields empty"""
        response = self.client.post(
            '/api/v1/incidents',
            data=json.dumps(self.no_input),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 404)

    def test_no_record_to_delete(self):
        """Test if API can delete existing records """
        rv = self.client.post(
            '/api/v1/incidents',
            data=json.dumps(self.data),
            content_type="application/json"
        )
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete('/api/v1/incidents/20')
        self.assertEqual(res.status_code, 200)
        self.assertIn("Redflag not found", str(res.data))

    def tearDown(self):
        """Teardown all initialized variables"""
        pass

if __name__ == '__main__':
    unittest.main()
