from django.contrib.auth import get_user_model
from django.conf import settings
from requests.exceptions import RequestException
import requests
import hashlib
import hmac
import string
import random
import time


class Trustpay:
    def oiij(self):
        self.TRUSTPAY_API_URL = settings.TRUSTPAY_API_URL
        self.TRUSTPAY_API_SECRET = settings.TRUSTPAY_API_SECRET
        self.TRUSTPAY_API_KEY = settings.TRUSTPAY_API_KEY

    def generate_random_string(self, length=15):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def send_pay_request(self, transaction, amount, first_name, email, phone, last_name="", address="Accra, Ghana",
                         city="Accra",
                         state="Greater Accra", country="Ghana"):
        return_url = (
            f"http://16.171.27.117/api/v1/transaction/confirm-pay/?orderId={transaction.id}&"
            f"invoice={transaction.serial_number}")
        cancel_url = (
            f"http://16.171.27.117/api/v1/transaction/cancel-pay/?orderId={transaction.id}&"
            f"invoice={transaction.serial_number}")
        base_url = self.TRUSTPAY_API_URL
        app_key = self.TRUSTPAY_API_KEY
        nounce = self.generate_random_string()
        timestamp = str(int(time.time()))

        message = (
                app_key + nounce + timestamp + amount + first_name + last_name + email + address + city +
                state + country + phone + return_url + cancel_url + transaction.serial_number +
                transaction.id
        ).replace(" ", "")

        signature = hmac.new(
            key=self.TRUSTPAY_API_SECRET,
            msg=message.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "x-app-key": app_key,
            "x-nonce": nounce,
            "x-timestamp": timestamp,
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
            response = requests.post(base_url + 'callgw', headers=headers, json=payload)
            # response.raise_for_status()
            print(response.json())
            if response.status_code == 200:
                return True
        except RequestException as e:
            print(e)
        return False

    def check_pay_success(self, transaction):
        return True
