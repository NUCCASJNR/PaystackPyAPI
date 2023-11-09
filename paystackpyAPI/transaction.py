#!/usr/bin/env python3

"""Handles All Paystack related tasks"""
import requests
from .base import PaystackAPI
from typing import Dict, Union
from errors import APIError


class Transaction(PaystackAPI):
    INITIALIZATION_OPTIONAL_PARAMS = [
        "currency",
        "reference",
        "callback_url",
        "plan",
        "invoice_limit",
        "metadata",
        "channels",
        "split_code",
        "subaccount",
        "transaction_charge",
        "bearer"
    ]

    TRANSACTION_LIST_OPTIONAL_PARAMS = [
        "customer",
        "terminalid",
        "status",
        "from",
        "to",
        "amount"
    ]

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.paystack_initialization_url = "https://api.paystack.co/transaction/initialize"
        self.paystack_verification_url = "https://api.paystack.co/transaction/verify"
        self.list_transaction_url = "https://api.paystack.co/transaction"

    def initialize_transaction(self, email: str, amount: int, **kwargs):
        """
        Initialize a Paystack transaction.

        :param email: Customer's email address.
        :param amount: Transaction amount.
        :param kwargs: Optional parameters for the transaction.
                       Example: `currency`, `callback_url`, etc.
        :return: JSON response from Paystack API.
        :raises APIError: If required parameters are missing or the API key is invalid.
        """
        if not email or not amount:
            raise APIError(400, "Missing required parameters: email and/or amount")

        valid_kwargs = {key: value for key, value in kwargs.items() if key in self.INITIALIZATION_OPTIONAL_PARAMS}
        data = {
            "email": email,
            "amount": amount,
            **valid_kwargs
        }

        if not self.api_key:
            raise APIError(401, "Invalid API key")

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        response = requests.post(self.paystack_initialization_url, headers=headers, json=data)
        if response.status_code == 200:
            custom_response = {
                "status_code": response.status_code,
                "message": "Transaction initialized successfully",
                "data": response.json()
            }
        else:
            error_message = response.text
            raise APIError(response.status_code, error_message)
        return custom_response

    def verify_transaction(self, reference: Union[int, str]) -> Dict:
        """
        Verify a Paystack transaction.

        :param reference: Reference id of the transaction (int or str).
        :return: Customized response from Paystack API.
        :raises APIError: If the reference is missing or the API key is invalid.
        """
        if not reference:
            raise APIError(400, "Missing required parameter: reference")

        if not self.api_key:
            raise APIError(401, "Invalid API key")

        url = f"{self.paystack_verification_url}/{reference}"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            custom_response = {
                "status_code": response.status_code,
                "message": "Transaction details retrieved successfully",
                "data": response.json()
            }
        else:
            error_message = response.text
            raise APIError(response.status_code, error_message)

        return custom_response

    def list_transactions(self, **kwargs: Dict) -> Dict:
        """
        Retrieve a list of transactions based on optional parameters.

        :param kwargs: Optional parameters for filtering the list of transactions.
                       Supported parameters:
                       - `perPage`: Number of transactions to retrieve per page.
                       - `page`: Page number for pagination.
                       - `from`: Start date for transactions in the format 'YYYY-MM-DD'.
                       - `to`: End date for transactions in the format 'YYYY-MM-DD'.
                       - `customer`: Customer's email or identification.
                       - `status`: Transaction status (e.g., 'success', 'failed').
                       - `currency`: Currency code (e.g., 'NGN', 'USD').
                       - `amount`: Transaction amount.
                       - `reference`: Transaction reference.
                       - `gateway`: Payment gateway used (e.g., 'card', 'bank').
                       - `channel`: Transaction channel (e.g., 'card', 'bank').
                       - `plan`: Plan code associated with the transaction.

        :return: Customized response with the list of transactions.
                 Format: {
                     "status_code": int,
                     "message": str,
                     "data": dict
                 }

        :raises APIError: If the API key is invalid or if there's an issue with the request.
        """
        if not self.api_key:
            raise APIError(401, "Invalid API Key")

        valid_kwargs = {key: value for key, value in kwargs.items() if key in self.TRANSACTION_LIST_OPTIONAL_PARAMS}

        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            **valid_kwargs
        }

        response = requests.get(self.list_transaction_url, headers=headers, params=data)

        if response.status_code == 200:
            custom_response = {
                "status_code": response.status_code,
                "message": "Transactions details below",
                "data": response.json()
            }
        else:
            error_message = response.text
            raise APIError(response.status_code, error_message)

        return custom_response

