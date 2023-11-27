from os import getenv
import requests

api_key = getenv("PAYSTACK_KEY")

url = "https://api.paystack.co/split"
authorization = f"Bearer {api_key}"
content_type = "application/json"
headers = {
    "Authorization": authorization,
    "Content-Type": content_type
}

data = {
    "name": "Percentage Split",
    "type": "percentage",
    "currency": "NGN",
    "subaccounts": [
        {
            "subaccount": "ACCT_j1ibmm5vpj5ior7",  # Replace with the actual subaccount code
            "share": 10  # Adjust the share percentage as needed
        },
        # Add other subaccounts as necessary
    ],
    "bearer_type": "subaccount",
    "bearer_subaccount": "ACCT_j1ibmm5vpj5ior7"  # Make sure this subaccount is part of the split group
}

response = requests.post(url, json=data, headers=headers)

print(response.status_code)
print(response.json())
