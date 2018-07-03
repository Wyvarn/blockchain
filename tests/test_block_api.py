import json
from tests import BaseTestCase
from unittest import main
from unittest.mock import MagicMock, patch


class BlockApiTestCases(BaseTestCase):
    """BlockAPI test cases"""

    def test_new_transaction_returns_201_on_post_request(self):
        """Test new transaction returns response of 201 for POST request with correct arguments"""
        response = self.client.post('/api/block/transactions/new', data=dict(
           sender="onluncd", recipient="bouncda", amount=100
        ))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Transaction will be added to block ', response.data.decode("utf-8"))

    @patch("app.mod_blockchain.views.uuid4", return_value=100)
    def test_mine_block_returns_200_on_post_request(self, mock_uuid):
        """Test POST request to mine block route returns 200 with block metadata"""
        response = self.client.post("/api/block/mine")
        self.assert200(response)

        mock_uuid.return_value = 100

        mock_node_identifier = str(mock_uuid()).replace("-", "")

        last_block = self.blockchain.last_block
        last_proof = last_block["proof"]
        proof = self.blockchain.proof_of_work(last_proof)

        self.blockchain.new_transaction(sender="0", recipient=mock_node_identifier, amount=1)

        previous_hash = self.blockchain.hash(last_block)
        block = self.blockchain.new_block(proof, previous_hash)

        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data.get("message"), "New block forged")
        self.assertEqual(data.get("index"), block["index"])
        self.assertEqual(data.get("proof"), block["proof"])

    def test_get_chain_returns_200_on_get_request(self):
        response = self.client.get("/api/block/chain")
        self.assert200(response)

        data = json.loads(response.data.decode("utf-8"))
        self.assertIn("chain", data)
        self.assertEqual(data.get("length"), len(self.blockchain))

    # def test_registration_returns_201_when_user_data_is_posted(self):
    #     """Test POST request with data to registration returns 201 response"""
    #     user = {'username': 'user3', 'password': 'user3_password', "email": "user3_email"}
    #     req = self.client.post('/auth/register/', data=user)
    #     self.assertEqual(req.status_code, 201)
    #
    # def test_registration_raises_exception_when_user_exists(self):
    #     """Test registration route raises Exception when user already exists"""
    #     user = {'username': 'user2', 'password': 'user2_password', "email": "user2_email"}
    #     with self.assertRaises(UserAlreadyExists) as context:
    #         self.client.post('/auth/register/', data=user)
    #         self.assertTrue(UserAlreadyExists.detail in context.exception)


# class LoginTestCases(BaseTestCase):
#     """ Tests correct user login"""
#
#     def test_correct_logging_in_returns_200(self):
#         """Test login route returns 200"""
#         response = self.login()
#         self.assert200(response)
#
#     def test_get_request_raises_credentials_required_error(self):
#         """Test GET request to login without credentials raises error"""
#         with self.assertRaises(CredentialsRequired) as context:
#             self.client.get("/auth/login/")
#             self.assertTrue(CredentialsRequired.detail in context.exception)
#
#     def test_get_request_with_correct_credentials_returns_response(self):
#         """Test GET request with correct credentials returns correct response"""
#         response = self.login()
#         self.assertIn(b'You have logged in successfully', response.data)
#
#     def test_incorrect_logging_in_returns_401(self):
#         """Tests incorrect user login will raise error"""
#         wrong_req = self.client.post('/auth/login/', data=dict(username="itsme",
#                                                                email="noclue@example.com",
#                                                                password="i have no idea"))
#         self.assert401(wrong_req)
#
#     def test_incorrect_credentials_raises_error(self):
#         """Tests incorrect user credentials raises error"""
#         with self.assertRaises(AuthenticationFailed) as context:
#             self.client.post('/auth/login/', data=dict(username="user1",
#                                                        email="user1@example.com",
#                                                        password="i have no idea"))
#             self.assertEqual(AuthenticationFailed.detail, context.exception)
#
#     def test_correct_credentials_logs_in_user_with_flask_login(self):
#         """Test correct credentials logs in user with flask login"""
#         with self.client:
#             self.login()
#             self.assertIsNotNone(current_user)
#             self.assertTrue(current_user.is_active)
#             self.assertTrue(current_user.is_authenticated)
#
#     def test_log_out_with_valid_jwt_token(self):
#         """Test user can correctly log out when passing JWT token in header"""
#         with self.client:
#             response = self.login()
#             json_response = json.loads(response.data.decode("utf-8"))
#             jwt_token = json_response.get("token")
#             headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
#             logout_response = self.client.get("/auth/logout/", headers=headers)
#             self.assertIn('You have logged out successfully', logout_response.data.decode("utf-8"))
#
#     def test_correct_token_generation(self):
#         """Tests correct token generation"""
#         rv = self.client.post("/auth/login/", data={'username': 'its-me', 'password': 'i have no idea'})
#         res_json = json.loads(rv.data.decode("utf-8"))
#         jwt_token = res_json.get('token')
#         self.assertIsNone(jwt_token)


if __name__ == "__main__":
    main()
