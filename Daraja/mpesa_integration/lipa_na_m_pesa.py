from datetime import datetime
import base64

import requests
from requests.auth import HTTPBasicAuth

# Key variables 
lipa_na_m_pesa_shortcode = "174379"
lipa_na_m_pesa_passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
phone_number = "254711994966"
consumer_key = "IvFkneOfx6S6sIgRHrqMtfJVNOGsF9n9"
consumer_secret = "19htvGwAXUXMAvGU"

# Getting timezone
raw_timestamp = datetime.now()
formatted_timestamp = raw_timestamp.strftime('%Y%m%d&H%M%S')
print(formatted_timestamp)

# Getting password : => base64&utf-8(lipa_na_m_pesa_shortcode + lipa_na_m_pesa_passkey + timestamp)
raw_password = lipa_na_m_pesa_shortcode + lipa_na_m_pesa_passkey + formatted_timestamp
password_encoded = base64.b64encode(raw_password.encode())
utf8_decoded_password = password_encoded.decode('utf-8')

# Getting access token
api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

r = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
json_response = r.json()
my_access_token = json_response['access_token']
print(my_access_token)

# Lipa na mpesa transaction
def lipa_na_mpesa():
    access_token = my_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "BusinessShortCode": lipa_na_m_pesa_shortcode,
        "Password": utf8_decoded_password,
        "Timestamp": formatted_timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1000",
        "PartyA": phone_number,
        "PartyB": lipa_na_m_pesa_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://fullstackdjango.com",
        "AccountReference": "37696611",
        "TransactionDesc": "Test payment"
    }
  
    response = requests.post(api_url, json = request, headers=headers)
  
    print(response.text)

#lipa_na_mpesa()        