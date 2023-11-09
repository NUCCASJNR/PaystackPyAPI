from paystackpyAPI.transaction import Transaction
"""
Purpose: Demonstrates a basic transaction initialization without
optional parameters.
"""
api_key = 'your_api_key'
transaction = Transaction(api_key)

email = 'user@example.com'
amount = 100
initialize_response = transaction.initialize_transaction(email, amount)
print("Initialization Response:", initialize_response)
