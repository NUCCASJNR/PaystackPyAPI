from errors import APIError


class PaystackAPI:
    
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
