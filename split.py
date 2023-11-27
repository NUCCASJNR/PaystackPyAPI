#!/usr/bin/env python3
from paystackpyAPI.transaction_splits import TransactionSplit
from os import getenv

api_key = getenv('PAYSTACK_KEY')
SPLIT_ID = ''
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
    SPLIT_ID = res["response_from_api"]["data"]["id"]
    # print(SPLIT_ID)
except Exception as e:
    print(f'Error: {str(e)}')

try:
    details = transaction.fetch_transaction_splits('SPLIT_ID')
    print(details)
except Exception as e:
    print(f'Error: {str(e)}')