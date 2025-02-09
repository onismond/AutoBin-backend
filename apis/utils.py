from django.contrib.auth import get_user_model
from django.conf import settings
from requests.exceptions import RequestException
import requests
import hashlib
import hmac
import string
import random
import time


def generate_random_string(length=15):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def send_pay_request(transaction, amount, first_name,  email, phone, last_name="", address="Accra, Ghana", city="Accra",
                     state="Greater Accra", country="Ghana"):
    return_url = (f"https://autobin-ucc-40b2bf6f03bc.herokuapp.com/api/v1/transaction/confirm-pay/?orderId={transaction.id}&"
                  f"invoice={transaction.serial_number}")
    cancel_url = (f"https://autobin-ucc-40b2bf6f03bc.herokuapp.com/api/v1/transaction/cancel-pay/?orderId={transaction.id}&"
                  f"invoice={transaction.serial_number}")
    base_url = settings.TRUSTPAY_API_URL

    message = (first_name + last_name).replace(" ", "")
    signature = hmac.new(
        key=settings.TRUSTPAY_API_SECRET,
        msg=message.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "x-app-key": settings.TRUSTPAY_API_KEY,
        "x-nonce": generate_random_string(),
        "x-timestamp": str(int(time.time())),
        "x-signature": signature,
        "amount": amount,
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "address": address,
        "city": city,
        "state": state,
        "country": country,
        "phone": phone,
        "returnUrl": return_url,
        "cancelUrl": cancel_url,
        "invoice": transaction.serial_number,
        "orderId": transaction.id,
    }
    try:
        response = requests.post(base_url, headers=headers, json=payload)
        response.raise_for_status()
        print(response.json())
        if response.status_code == 200:
            return True
    except RequestException as e:
        print(e)
    return False



def check_pay_success(transaction):
    return True