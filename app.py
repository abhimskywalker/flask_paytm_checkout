import datetime
import logging

import requests
from flask import Flask, render_template, request

from paytm_checksum import generate_checksum, verify_checksum

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Staging configs:
# Keys from https://dashboard.paytm.com/next/apikeys
# MERCHANT_ID = "cqxpFk55774655560618"
# MERCHANT_KEY = "4a%G!gRDQrao6eC1"
# WEBSITE_NAME = "WEBSTAGING"
# INDUSTRY_TYPE_ID = "Retail"
# BASE_URL = "https://securegw-stage.paytm.in"


# Production configs:
# Keys from https://dashboard.paytm.com/next/apikeys
MERCHANT_ID = "<MERCHANT_ID>"
MERCHANT_KEY = "<MERCHANT_KEY>"
WEBSITE_NAME = "<WEBSITE_NAME>"
INDUSTRY_TYPE_ID = "<INDUSTRY_TYPE_ID>"
BASE_URL = "https://securegw.paytm.in"


@app.route("/")
def index():
    amount = 11.07
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

    # Generate checksum hash
    transaction_data["CHECKSUMHASH"] = generate_checksum(transaction_data, MERCHANT_KEY)

    logging.info("Request params: {transaction_data}".format(transaction_data=transaction_data))

    url = BASE_URL + '/theia/processTransaction'
    return render_template("index.html", data=transaction_data, url=url)


@app.route('/callback', methods=["GET", "POST"])
def callback():
    # log the callback response payload returned:
    callback_response = request.form.to_dict()
    logging.info("Transaction response: {callback_response}".format(callback_response=callback_response))

    # verify callback response checksum:
    checksum_verification_status = verify_checksum(callback_response, MERCHANT_KEY,
                                                   callback_response.get("CHECKSUMHASH"))
    logging.info("checksum_verification_status: {check_status}".format(check_status=checksum_verification_status))

    # verify transaction status:
    transaction_verify_payload = {
        "MID": callback_response.get("MID"),
        "ORDERID": callback_response.get("ORDERID"),
        "CHECKSUMHASH": callback_response.get("CHECKSUMHASH")
    }
    url = BASE_URL + '/order/status'
    verification_response = requests.post(url=url, json=transaction_verify_payload)
    logging.info("Verification response: {verification_response}".format(
        verification_response=verification_response.json()))

    return render_template("callback.html",
                           callback_response=callback_response,
                           checksum_verification_status=checksum_verification_status,
                           verification_response=verification_response.json())
