from paystackpyAPI.transaction import Transaction
"""
Purpose: Shows how to include optional parameters
in the transaction initialization.
"""
api_key = 'your_api_key'
transaction = Transaction(api_key)

email = 'user@example.com'
amount = 100
options = {
    'currency': 'USD',
    'callback_url': 'https://example.com/callback',
    # ... other optional parameters ...
}
initialize_response = transaction.initialize_transaction(email, amount, **options)
print("Initialization Response:", initialize_response)
