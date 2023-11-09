# PaystackPyAPI

PaystackPyAPI is a Python package designed to simplify and streamline Paystack API integration, enabling secure online payment processing in your Python applications.

## Installation

You can install the package using pip:

```bash
pip install paystackpyAPI
```

##  Getting Started

**1. Obtain API Key:**

_Sign up for a Paystack account if you don't have one: [Paystack Signup](https://dashboard.paystack.com/signup).

_Log in to your Paystack dashboard and obtain your API key._

2. **Initialize PaystackAPI:**

```bash
from paystackpyAPI.transaction import Transaction

# Replace 'your_api_key' with your actual Paystack API key
api_key = 'your_api_key'
transaction = Transaction(api_key)

```

3. **Initialize a Transaction**

```bash
email = 'user@example.com'
amount = 100
initialize_response = transaction.initialize_transaction(email, amount)
print("Initialization Response:", initialize_response)
```

4. **Verify a Transaction**
```bash
reference = initialize_response['data']['data']['reference']
verify_response = transaction.verify_transaction(reference)
print("Verification Response:", verify_response)

```

5. **Optional parameters**

_The initialize_transaction method supports the following optional parameters:

1. currency

2. reference

3. callback_url

4. plan

5. invoice_limit

6. metadata

7. channels

8. split_code

9. subaccount

10. transaction_charge

11. bearer

Pass these parameters as keyword arguments when calling the initialize_transaction method.

6. **Examples**

Check the [examples](./examples) directory for sample scripts demonstrating various use cases.

7. **Contributing**

_If you find a bug or have a feature request, please open an issue. Contributions are welcome!_
    
    1. Fork the repository
    2. Create a new branch (git checkout -b feature/awesome-feature).
    3. Commit your changes (git commit -am 'Add awesome feature').
    4. Push to the branch (git push origin feature/awesome-feature).
    5. Open a Pull Request.

8. **License**

_This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details._