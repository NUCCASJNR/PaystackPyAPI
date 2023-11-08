import unittest
from paystackpy.api import PaystackAPI
from os import getenv
import secrets

REFERENCE = secrets.token_hex(16)
class TestPaystackAPI(unittest.TestCase):
    def setUp(self):
        # Set up any necessary test data or configurations
        self.api = PaystackAPI(getenv("PAYSTACK_KEY"))

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
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["message"], "Transaction details retrieved successfully")

if __name__ == '__main__':
    unittest.main()
