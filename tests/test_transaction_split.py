#!/usr/bin/env python3
from paystackpyAPI.transaction_splits import TransactionSplit
from errors import APIError

import unittest
from os import getenv

api_key = getenv("PAYSTACK_KEY")


class TestPaystackAPISplit(unittest.TestCase):
    def setUp(self):
        self.api = TransactionSplit(api_key=api_key)

    def tearDown(self):
        self.api.close()

    def test_transaction_split(self):
        try:
            split_name = "Test Split"
            split_type = "percentage"
            split_currency = "NGN"
            split_subaccounts = [
                {"subaccount": "ACCT_j1ibmm5vpj5ior7", "share": 20}
            ]
            split_bearer_type = "subaccount"
            split_bearer_subaccount = "ACCT_j1ibmm5vpj5ior7"
            res = self.api.create_split(split_name, split_type, split_currency,
                                        split_subaccounts, split_bearer_type, split_bearer_subaccount)
            self.assertEqual(res["status_code"], 200)
            self.assertEqual(res["message"], "Transaction initialized successfully")
            self.assertEqual(res["response_from_api"]["status"], True)
            self.assertEqual(res["response_from_api"]["message"], "Split created")
        finally:
            self.api.close()
