import base64
from datetime import datetime
from encodings.base64_codec import base64_encode

import keys
import requests
from requests.auth import HTTPBasicAuth

# Generating the Timestamp
raw_timestamp = datetime.now()
formatted_timestamp = raw_timestamp.strftime("%Y%m%d%H%M%S") #strftime converts datetime into string, strptime converts string into datetime 

# Generating password
raw_password = keys.shortcode + keys.lipa_na_mpesa_pass_key + formatted_timestamp 
encoded_password = base64.b64encode(raw_password.encode())
utf_formatted_password = encoded_password.decode("utf-8")
# print(utf_formatted_password)

# Generating access token
consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

r = requests.get(api_url, auth = HTTPBasicAuth(consumer_key,consumer_secret))
#print(r.text)
json_response = r.json()
my_access_token = json_response['access_token']

def lipa_na_mpesa():
    access_token = my_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "BusinessShortCode": keys.shortcode,
        "Password": utf_formatted_password,
        "Timestamp": formatted_timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "10",
        "PartyA": keys.phone_number,
        "PartyB": keys.shortcode,
        "PhoneNumber": keys.phone_number,
        "CallBackURL": "https://kenova.co",
        "AccountReference": "37696611",
        "TransactionDesc": "Test payment"
    }
  
    response = requests.post(api_url, json = request, headers=headers)
  
    print(response.text)

lipa_na_mpesa()
