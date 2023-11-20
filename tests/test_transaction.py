import tracemalloc
import unittest
from unittest.mock import Mock, patch
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
        self.api.close()

    def test_non_200_response(self):
        try:
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
        finally:
            self.api.close()

    def test_initialize_transaction(self):
        try:
            data = {
                "email": "test@example.com",
                "amount": 1000,
                "reference": REFERENCE,
            }

            response = self.api.initialize_transaction(**data)
            self.assertEqual(response["status_code"], 200)
            self.assertEqual(response["message"], "Transaction initialized successfully")
            print(response["message"])
        finally:
            self.api.close()

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

    def test_authorize_transaction_with_missing_amount(self):
        data = {
            "email": "alareefadegbite@gmail.com",
            "authorization_code": "AUTH_8dfhjjdt",
            "amount": None
        }
        with self.assertRaises(APIError) as context:
            self.api.charge_authorization(**data)
        print(context.exception)
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Missing required parameter amount", str(context.exception))

    def test_authorize_transaction_with_missing_email(self):
        data = {
            "email": None,
            "authorization_code": "AUTH_8dfhjjdt",
            "amount": 2000
        }
        with self.assertRaises(APIError) as context:
            self.api.charge_authorization(**data)
        print(context.exception)
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Missing required parameter email", str(context.exception))

    def test_authorize_transaction_with_missing_auth_code(self):
        data = {
            "email": 'alareefadegbite@gmail.com',
            "authorization_code": None,
            "amount": 2000
        }
        with self.assertRaises(APIError) as context:
            self.api.charge_authorization(**data)
        print(context.exception)
        self.assertEqual(context.exception.status_code, 400)
        self.assertIn("Missing required parameter auth", str(context.exception))

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

    def test_get_transaction_totals(self):
        response = self.api.get_total_transactions()
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["message"], "Transaction totals retrieved successfully")
        print(response["message"])

    def test_get_transaction_totals_with_400(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                self.api.transaction_totals_url,
                status=400,
                json={"status": False, "message": "Invalid request"},
            )
            with self.assertRaises(APIError) as context:
                self.api.get_total_transactions()
            self.assertEqual(context.exception.status_code, 400)
            self.assertIn("Invalid request", str(context.exception))

    def test_get_transaction_totals_with_401(self):
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                self.api.transaction_totals_url,
                status=401,
                json={"status": False, "message": "Invalid API Key"},
            )
            with self.assertRaises(APIError) as context:
                self.api.get_total_transactions()
            self.assertEqual(context.exception.status_code, 401)
            self.assertIn("Invalid API Key", str(context.exception))
    
    def test_export_transactions(self):
        response = self.api.export_transactions()
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["message"], 'Transactions exported successfully to export.csv')
        self.assertEqual(response['data'], {'exported_file': 'export.csv'})

    @patch('paystackpyAPI.transaction.requests.get')
    def test_export_transaction_failure(self, mock_get):
        mock_get.return_value.status = 404
        mock_get.return_value.text = 'Not Found'
        try:
            self.api.export_transactions()
        except APIError as e:
            self.assertEqual(e.status_code, 404)
            self.assertEqual(e.message, 'Not Found')

if __name__ == '__main__':
    unittest.main()
