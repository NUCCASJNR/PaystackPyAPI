from paystackpyAPI.transaction import Transaction
"""
Purpose: Illustrates how to verify a transaction using the verify_transaction method.
"""
api_key = 'your_api_key'
transaction = Transaction(api_key)

# Replace 'your_reference' with an actual reference from a previous initialization
reference = 'your_reference'
verify_response = transaction.verify_transaction(reference)
print("Verification Response:", verify_response)
