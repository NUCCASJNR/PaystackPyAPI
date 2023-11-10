import tracemalloc
import unittest
from paystackpyAPI.transaction import Transaction
from errors import APIError
from os import getenv
import secrets
import responses

REFERENCE = secrets.token_hex(16)
ID = ''
print(ID)
class TestPaystackAPI(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        self.api = Transaction(api_key=getenv("PAYSTACK_KEY"))

    def tearDown(self):
        # Clean up any resources used for testing
        responses.stop()
        responses.reset()
        tracemalloc.stop()

    def test_non_200_response(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                self.api.paystack_initialization_url,
                status=400,
                json={"status": False, "message": "Invalid request"},
            )
            data = {
                "email": "test@example.com",
                "amount": 1000,
                "reference": REFERENCE,
            }
            with self.assertRaises(APIError) as context:
                self.api.initialize_transaction(**data)
            self.assertEqual(context.exception.status_code, 400)

    def test_initialize_transaction(self):
        data = {
            "email": "test@example.com",
            "amount": 1000,
            "reference": REFERENCE,
        }

        response = self.api.initialize_transaction(**data)
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["message"], "Transaction initialized successfully")
        print(response["message"])

    def test_verify_transaction(self):
        reference = REFERENCE
        response = self.api.verify_transaction(reference)
        ID = response["response_from_api"]['data']['id']
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["message"], "Transaction details retrieved successfully")

    def test_invalid_reference_key(self):
        reference = "invalid_reference"
        with self.assertRaises(APIError):
            self.api.verify_transaction(reference)

    def test_missing_email_initialize(self):
        with self.assertRaises(APIError) as context:
            self.api.initialize_transaction(amount=1000, email=None)
        # self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Missing required parameters: email and/or amount", str(context.exception))

    def test_missing_amount_initialize(self):
        with self.assertRaises(APIError) as context:
            self.api.initialize_transaction(amount=None, email="idan@gmail.com")
        # self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Missing required parameters: email and/or amount", str(context.exception))

    def test_missing_reference_verify(self):
        with self.assertRaises(APIError) as context:
            self.api.verify_transaction(reference=None)
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Missing required parameter: reference", str(context.exception))

    def test_list_transactions(self):
        response = self.api.list_transactions()
        if response["status_code"] == 401:
            self.assertEqual(response["message"], "Invalid API key")
        elif response["status_code"] == 200:
            self.assertEqual(response["status_code"], 200)
            self.assertEqual(response["message"], "Transactions details below")

    def test_with_str_id(self):
        with self.assertRaises(APIError) as context:
            self.api.fetch_transaction("wrong_id")
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Transaction ID should be numeric", str(context.exception))

    def test_with_int_id(self):
        with self.assertRaises(APIError) as context:
            self.api.fetch_transaction(123456789)
        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Transaction not found", str(context.exception))
        print(str(context.exception))

    def test_with_valid_id(self):
        response = self.api.fetch_transaction(ID)
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["message"], "Transaction Successfully fetched")
        print(response["message"])

    def test_show_transaction_timeline_with_wrongId(self):
        with self.assertRaises(APIError) as context:
            self.api.show_transaction_timeline("wrong_id")
        self.assertEqual(context.exception.status_code, 404)
        self.assertIn("Transaction ID or reference is invalid", str(context.exception))

    def test_show_transaction_timeline_with_validId(self):
        response = self.api.show_transaction_timeline(REFERENCE)
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["message"], "Transaction timeline retrieved")
        print(response["message"])


if __name__ == '__main__':
    unittest.main()
