# import os 
# import unittest
# import json 
# import pytest

# from ... import create_app


# class TestAuthorization(unittest.TestCase):
#     """ Test for the user authentication """

#     def setUp(self):
#         """Defines the test variables. """
#         self.app = create_app(config_name="testing")
#         self.client = self.app.test_client()
#         self.auth = {
#             "firstname": "Anjichi",
#             "lastname": "Lupamo",
#             "othernames": "R",
#             "username": "Andela1",
#             "email": "andela@andela.andela",
#             "phonenumber": "0717245777",
#             "password": "Eatlivecode"
#         }

    

#     def test_user_signup(self):
#         """Test to see user signing up"""
#         res = self.client.post(
#             '/signup', 
#             data=json.dumps(self.auth),
#             content_type="application/json"
#         )
#         result = json.loads(res.data.decode)
#         self.assertEqual(res.status_code,  200)
#         self.assertEqual(
#             result['message'], "You registerdd successfully, please login.")
#         self.assertEqual(res.status_code, 201)


#     def test_user_login(self):
#         """ Test that registered users can login """
#         res = self.client.post(
#             '/signup',
#             data=self.auth
#         )
#         self.assertEqual(res.status_code, 201)
#         login_res = self.client.post(
#             '/login',
#             data=self.auth
#         )
#         result = json.loads(login_res.data.decode())
#         self.assertEqual(result['message'], "You logged in successfully.")
#         self.assertEqual(login_res.status_code, 200)
#         self.assertTrue(result['access_token'])

#     def tearDown(self):
#         pass


# if __name__ == "__main__":
#     unittest.main()
