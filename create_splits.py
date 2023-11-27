#!/usr/bin/env python3
from paystackpyAPI.transaction_splits import TransactionSplit
from os import getenv

api_key = getenv('PAYSTACK_KEY')

transaction = TransactionSplit(api_key=api_key)

split_name = "Test Split"
split_type = "percentage"
split_currency = "NGN"
split_subaccounts = [
    {"subaccount": "ACCT_j1ibmm5vpj5ior7", "share": 20}
]
split_bearer_type = "subaccount"
split_bearer_subaccount = "ACCT_j1ibmm5vpj5ior7"
try:
    res = transaction.create_split(split_name, split_type, split_currency,
                                   split_subaccounts, split_bearer_type, split_bearer_subaccount)
    print(res)
except Exception as e:
    print(f'Error: {str(e)}')