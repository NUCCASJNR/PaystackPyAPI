#!/usr/bin/env python3

"""
The Transaction Splits API enables merchants split the settlement for a
transaction across their payout account,
and one or more subaccounts.
"""

from paystackpyAPI.base import PaystackAPI
from typing import Dict, List
from errors import APIError


class TransactionSplit(PaystackAPI):
    def __init__(self, api_key: str):
        """
        Initialization method
        api_key: Paystack API key used for Authentication
        """
        super().__init__(api_key)
        self.create_split_url = "https://api.paystack.co/split"

    def create_split(self, name: str, type: str, currency: str, subaccounts: List,
                     bearer_type: str, bearer_subaccount: str) -> Dict:
        """
        name: Name of transaction split
        type: The type of transaction split you want to create.
            You can use one of the following: percentage | flat
        currency: Any of the supported Currency
        subaccounts: A list of object containing subaccount code and number of shares:
            [{subaccount: ‘ACT_xxxxxxxxxx’, share: xxx},{...}]
        bearer_type: Any of subaccount | account | all-proportional | all
        bearer_subaccount: Subaccount code
        """

        if not self.api_key:
            raise APIError(401, "Invalid API Key")
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }

        data = {
            "name": name,
            "type": type,
            "currency": currency,
            "subaccount": subaccount,
            "bearer_type": subaccount,
            "bearer_subaccount": bearer_subaccount
        }
