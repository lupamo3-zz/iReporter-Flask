import os
import unittest
import json
import pytest

from ... import create_app


class TestRedflags(unittest.TestCase):
    """This class represents the test redflag case """

    def setUp(self):
        """Defines the test variables """

        self.app = create_app()
        self.client = self.app.test_client()
        self.data = {
            "createdOn": "2018-11-29 05:21:37",
            "createdBy": "Norbert",
            "location": "Mount Sinai",
            "status": "There is a bush on fire",
            "comment": "How hot can it be?",
            "id": 1
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
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    

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

    def tearDown(self):
        """Teardown all initialized variables"""
        pass


if __name__ == '__main__':
    unittest.main()
