
class PaystackError(Exception):
    """Base class for Paystack API errors."""

class APIError(PaystackError):
    """Exception raised for errors in the Paystack API.

    Attributes:
        status_code -- the HTTP status code indicating the error
        error_message -- a description of the error
    """

    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message
        super().__init__(self.error_message)
