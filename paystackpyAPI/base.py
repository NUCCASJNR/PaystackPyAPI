import requests
class PaystackAPI:
    
    def __init__(self, api_key: str) -> None:
        self.session = requests.Session()
        self.api_key = api_key
        
        
    def close(self):
        """
        Close the session and release associated resources.
        """
        if self.session:
            self.session.close()
            self.session = None