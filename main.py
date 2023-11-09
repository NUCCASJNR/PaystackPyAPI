from paystackpyAPI.transaction import Transaction
from os import getenv
api_key = getenv("PAYSTACK_KEY")

transaction_api = Transaction(api_key)

# Example: Initialize a transaction
email = 'customer@example.com'
amount = 5000  # Replace with your desired amount
optional_params = {'currency': 'NGN', 'callback_url': 'https://example.com/callback'}

try:
    initialization_response = transaction_api.initialize_transaction(email, amount, **optional_params)
    print("Initialization Response:", initialization_response)

    # Extract the reference from the initialization response
    reference_to_verify = initialization_response["response_from_api"]['data']['reference']

    # Example: Verify the transaction using the obtained reference
    try:
        verification_response = transaction_api.verify_transaction(reference_to_verify)
        print("Verification Response:", verification_response)
    except Exception as e:
        print("Error verifying transaction:", str(e))

    try:
        transactions = transaction_api.list_transactions()
        print("Transactions:", transactions)
    except Exception as e:
        print("Error listing transactions:", str(e))
    try:
        transaction_id = verification_response["response_from_api"]['data']['id']
        fetch_transaction = transaction_api.fetch_transaction(transaction_id)
        print("Transaction:", fetch_transaction)
    except Exception as e:
        print("Error fetching transaction:", str(e))

except Exception as e:
    print("Error initializing transaction:", str(e))
