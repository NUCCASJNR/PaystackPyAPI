import requests
from typing import Dict
from paystackpy.errors import APIError

class PaystackApi:
    
    ALLOWED_OPTIONAL_PARAMS = [
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
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.paystack_initilization_url = "https://api.paystack.co/transaction/initialize"
        self.paystack_verification_url = f"https://api.paystack.co/transaction/verify/"
        
    
    def initialize_transaction(self, email: str, amount: int, **kwargs):
        """
        Initialize a Paystack transaction.

        :param email: Customer's email address.
        :param amount: Transaction amount.
        :param kwargs: Optional parameters for the transaction.
                       Example: `currency`, `callback_url`, etc.
        :return: JSON response from Paystack API.
        """
        valid_kwargs = {key: value for key, value in kwargs.items() if key in self.ALLOWED_OPTIONAL_PARAMS}
        data = {
            "email": email,
            "amount": amount,
            **valid_kwargs
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.paystack_initilization_url, data=data, headers=headers)
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
    
    
    def verify_transaction(self, reference: int | str) -> Dict:
        """"""
