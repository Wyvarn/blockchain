import json
from tests import BaseTestCase
from unittest import main, skip
from unittest.mock import MagicMock, patch


class BlockApiTestCases(BaseTestCase):
    """BlockAPI test cases"""

    def test_new_transaction_returns_201_on_post_request(self):
        """Test new transaction returns response of 201 for POST request with correct arguments"""
        response = self.client.post('/api/block/transactions/new', json=dict(
           sender="onluncd", recipient="bouncda", amount=100
        ))
        self.assertEqual(response.status_code, 201)
        self.assertIn('Transaction will be added to block ', response.data.decode("utf-8"))

    def test_new_transaction_returns_400_on_invalid_post_request(self):
        """Test new transaction returns 400 on invalid sender address"""
        # if sender is None
        sender = None

        response = self.client.post('/api/block/transactions/new', json=dict(
           sender=sender, recipient="bouncda", amount=100
        ))

        self.assert400(response)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data.get("message"), "Missing values")

        # if recipient is None
        recipient = None

        response = self.client.post('/api/block/transactions/new', json=dict(
           sender="randomaddress", recipient=recipient, amount=100
        ))

        self.assert400(response)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data.get("message"), "Missing values")

        # if amount is None
        amount = None

        response = self.client.post('/api/block/transactions/new', json=dict(
           sender="randomaddress", recipient="randomAddress", amount=amount
        ))

        self.assert400(response)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(data.get("message"), "Missing values")

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

    def test_register_nodes_returns_201_on_successful_post_request(self):
        """Test that POST request with valid nodes returns 201 with message and total_nodes"""
        nodes = [
            "http://192.168.1.0:8000"
        ]

        response = self.client.post("/api/block/nodes/register", json=dict(nodes=nodes), headers=self.headers)

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data.decode("utf-8"))

        self.assertEqual(data.get("message"), "New nodes have been added")

        self.assertEqual(len(data.get("total_nodes")), len(nodes))

    def test_register_nodes_returns_400_on_failed_post_request(self):
        """Test that POST request returns 400 on invalid POST request"""
        nodes = None

        response = self.client.post("/api/block/nodes/register", json=dict(nodes=nodes))

        self.assert400(response)

        data = json.loads(response.data.decode("utf-8"))

        self.assertEqual(data.get("message"), "Error: Please supply a valid list of nodes")

    @skip("Execution takes long due to resolving of nodes, need to mock the resolve conflicts method from blockchain")
    def test_resolve_nodes_returns_200_on_successful_get_request(self):
        """Test GET request to nodes/resolve returns 200 with message and chain"""

        response = self.client.get("/api/block/nodes/resolve")
        self.assert200(response)

        data = json.loads(response.data.decode("utf-8"))

        self.assertIn("Our Chain", data)
        self.assertIn("chain", data)


if __name__ == "__main__":
    main()
