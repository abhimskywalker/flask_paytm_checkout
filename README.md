# Using Paytm Checkout and Flask
Integrate Paytm Checkout to your Python Flask website to provide a secure, PCI-compliant way to accept Debit/Credit card, Net-Banking, UPI and Paytm wallet payments from your customers.

# Setup steps
You’ll need to have the following prerequisites before we go any further:
- A [Paytm Merchant](https://business.paytm.com/) account
- A [Python](http://www.python.org/) environment

### 1. Basic app setup
```bash
# clone this repo from github
git clone https://github.com/abhimskywalker/flask_paytm_checkout.git
# navigative into the folder
cd flask_paytm_checkout
# install the requirements
pip install flask
pip install requests
easy_install pycrypto
```

### 2. Get merchant credentials
- Go to https://dashboard.paytm.com/next/apikeys to get your API keys
> These API keys consists of:
> - MID (Merchant ID): Unique identifier issued to every merchant.
> - Merchant Key: This is a unique secret key used for secure encryption of every request. This needs to be kept on server side and should never be shared with anyone.
> - Industry Type ID: This is part of bank and paymode configuration done wrt to an account.
> - Website: This parameter is used to support multiple callback URLs to post the transaction response. Each URL needs to be mapped to a website parameter.
- Copy the test MERCHANT_ID and test MERCHANT_KEY for testing mode in the Staging configs section. (While production configs are commented out)
- To do actual payments you can copy the MERCHANT_ID, MERCHANT_KEY, WEBSITE_NAME and INDUSTRY_TYPE_ID from Production API details tab. (Please comment out staging configs for this) 
- Replace the variables in `app.py`

### 3. Run the flask app
```bash
# run the flask app
FLASK_APP=app.py FLASK_ENV=development flask run
```
- Navigate to http://127.0.0.1:5000
- It will show the params that will be sent to Paytm server to initiate checkout flow includeing callback url (More detailed understanding availabel at: https://developer.paytm.com/docs/v1/payment-gateway )
- Once the transaction is done you will be redirected to http://127.0.0.1:5000/callback with checkout response params and then transaction verification API response params.
- Please note order id is auto generated based on timestamp for now. You can supply your own order details here later. Right now sample customer details (only recommended for testing) being sent as below:
```python
transaction_data = {
    "MID": MERCHANT_ID,
    "WEBSITE": WEBSITE_NAME,
    "INDUSTRY_TYPE_ID": INDUSTRY_TYPE_ID,
    "ORDER_ID": str(datetime.datetime.now().timestamp()),
    "CUST_ID": "007",
    "TXN_AMOUNT": str(amount),
    "CHANNEL_ID": "WEB",
    "MOBILE_NO": "7777777777",
    "EMAIL": "example@paytm.com",
    "CALLBACK_URL": "http://127.0.0.1:5000/callback"
}
```

### 4. Monitor the transactions on merchant dashboard
- Once a transaction is done in the above flow, you can check the details at: https://dashboard.paytm.com/next/transactions
