#!/usr/bin/env python3

"""Handles All Paystack related tasks"""
import requests
from paystackpyAPI.base import PaystackAPI
from typing import Dict, Union
from errors import APIError
from decimal import Decimal
import datetime
import webbrowser

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
    CHARGE_AUTHORIZATION_OPTIONAL_PARAMS = [
        "reference",
        "currency",
        "metadata",
        "channels",
        "subaccount",
        "transaction_charge",
        "bearer",
        "queue"
    ]
    
    EXPORT_OPTIONAL_PARAMS = [
        'from',
        'to',
        'customer',
        'status',
        'currency',
        'amount',
        'settled',
        'settlement',
        'payment_page'
    ]

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.session = requests.Session()
        self.paystack_initialization_url = "https://api.paystack.co/transaction/initialize"
        self.paystack_verification_url = "https://api.paystack.co/transaction/verify"
        self.list_transaction_url = "https://api.paystack.co/transaction"
        self.fetch_transaction_url = "https://api.paystack.co/transaction"
        self.charge_authorization_url = "https://api.paystack.co/transaction/charge_authorization"
        self.transaction_timeline_url = "https://api.paystack.co/transaction/timeline"
        self.transaction_totals_url = "https://api.paystack.co/transaction/totals"
        self.export_transactions_url = "https://api.paystack.co/transaction/export"
    
    def close(self):
        """
        Close the session and release associated resources.
        """
        if self.session:
            self.session.close()
            self.session = None
        

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
            "amount": amount * 100,
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
                "response_from_api": response.json()
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
                "response_from_api": response.json()
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
                "response_from_api": response.json()
            }
        else:
            error_message = response.text
            raise APIError(response.status_code, error_message)

        return custom_response

    def fetch_transaction(self, id: int) -> Dict:
        """
        Fetches the details of  a transaction using the id provided
        :param id:
            Transaction Id
        """
        if not self.api_key:
            raise APIError(401, "Invalid Api Key")
        url = f"{self.fetch_transaction_url}/{id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            custom_response = {
                "status_code": response.status_code,
                "message": "Transaction Successfully fetched",
                "response_from_api": response.json()
            }
        else:
            error_message = response.text
            raise APIError(response.status_code, error_message)
        return custom_response

    def charge_authorization(self, email: str, amount: int, authorization_code: str, **kwargs: Dict) -> Dict:
        """charge  a transaction"""

        if not self.api_key:
            raise APIError(401, "Invalid API Key")
        valid_kwargs = {key: value for key, value in kwargs.items() if key in self.CHARGE_AUTHORIZATION_OPTIONAL_PARAMS}
        if not amount:
            raise APIError(400, "Missing required parameter amount")
        if not email:
            raise APIError(400, "Missing required parameter email")
        if not authorization_code:
            raise APIError(400, "Missing required parameter authorization_code")
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        data = {
            "email": email,
            "amount": amount * 100,
            "authorization_code": authorization_code,
            **valid_kwargs
        }
        response = requests.post(self.charge_authorization_url, headers=headers, json=data)
        if response.status_code == 200:
            custom_response = {
                "status_code": response.status_code,
                "message": "Transaction initialized successfully",
                "response_from_api": response.json()
            }
        else:
            error_message = response.text
            raise APIError(response.status_code, error_message)
        return custom_response

    def show_transaction_timeline(self, id_or_reference: str) -> Dict:
        """
        SHow a transaction timeline
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f"{self.transaction_timeline_url}/{id_or_reference}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            custom_response = {
                "status_code": response.status_code,
                "message": "Transaction timeline retrieved",
                "response_from_api": response.json()
            }
        else:
            error_message = response.text
            raise APIError(response.status_code, error_message)
        return custom_response

    def get_total_transactions(self, per_page=50, page=1, from_date=None, to_date=None):
        """
        Retrieve the total amount received on your account based on specified parameters.

        :param per_page: Number of records to retrieve per page (default is 50).
        :param page: Page number to retrieve (default is 1).
        :param from_date: Start date for listing transactions in the format 'YYYY-MM-DDTHH:mm:ss.SSSZ'.
        :param to_date: End date for listing transactions in the format 'YYYY-MM-DDTHH:mm:ss.SSSZ'.

        :return: Customized response with the total amount received.
                 Format: {
                     "status_code": int,
                     "message": str,
                     "data": {
                         "total_amount": float
                     }
                 }

        :raises APIError: If the API key is invalid or if there's an issue with the request.
        """
        if not self.api_key:
            raise APIError(401, "Invalid API Key")

        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        params = {
            'perPage': per_page,
            'page': page,
            'from': from_date,
            'to': to_date
        }

        response = requests.get(self.transaction_totals_url, headers=headers, params=params)

        if response.status_code == 200:
            custom_response = {
                "status_code": response.status_code,
                "message": "Transaction totals retrieved successfully",
                "response_from_api": response.json()
            }
        else:
            error_message = response.text
            raise APIError(response.status_code, error_message)

        return custom_response
    
    def download_csv(self, url, output_filename='exported_file.csv'):
        response = requests.get(url)
        response.raise_for_status()

        with open(output_filename, 'wb') as file:
            file.write(response.content)

        print(f'File downloaded successfully: {output_filename}')

    def export_transactions(self, per_page=50, page=1, filename="export.csv", **kwargs):
        """
        initiate the export, and download the CSV file.

        :param per_page: Number of records to retrieve per page (default is 50).
        :param page: Page number to retrieve (default is 1).
        :param filename: Optional filename for the exported CSV file.

        :return: Customized response indicating the success of the export.
                 Format: {
                     "status_code": int,
                     "message": str,
                     "data": {
                         "exported_file": str  # File path or URL
                     }
                 }

        :raises APIError: If the API key is invalid, export initiation fails, or if there's an issue with the request.
        """
        optional_kwargs = {key: value for key, value in kwargs.items() if key in self.EXPORT_OPTIONAL_PARAMS}
        if not self.api_key:
            raise APIError(401, "Invalid API key")
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        params = {
            'perPage': per_page,
            'page': page,
            **optional_kwargs
        }
        try:
            response = requests.get(self.export_transactions_url, headers=headers, params=params)
            if response.status_code == 200:
               data = response.json()
               url_to_visit = data['data']['path']
            #    webbrowser.open(url_to_visit)
               self.download_csv(url_to_visit, output_filename=filename)

            custom_response = {
                "status_code": response.status_code,
                "message": f"Transactions exported successfully to {filename or url_to_visit}",
                "data": {
                    "exported_file": filename or url_to_visit
                }
            }

            return custom_response
        

        except requests.exceptions.HTTPError as errh:
            raise APIError(errh.response.status_code, f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            raise APIError(500, f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            raise APIError(500, f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            raise APIError(500, f"An error occurred: {err}")
