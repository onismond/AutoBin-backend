from django.conf import settings
from requests.exceptions import RequestException
import requests
import hashlib
import hmac
import string
import random
import time


class Trustpay:
    def __init__(self):
        self.TRUSTPAY_API_URL = settings.TRUSTPAY_API_URL
        self.TRUSTPAY_API_SECRET = settings.TRUSTPAY_API_SECRET
        self.TRUSTPAY_API_KEY = settings.TRUSTPAY_API_KEY

    def generate_random_string(self, length=15):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def send_pay_request(self, transaction, first_name, email, phone, last_name="last", address="Accra Road",
                         city="Accra",
                         state="Accra", country="84"):
        return_url = (
            f"http://13.53.168.208/api/v1/transaction/confirm-pay/?orderId={transaction.id}&"
            f"invoice={transaction.serial_number}")
        cancel_url = (
            f"http://13.53.168.208/api/v1/transaction/cancel-pay/?orderId={transaction.id}&"
            f"invoice={transaction.serial_number}")
        base_url = self.TRUSTPAY_API_URL
        app_key = self.TRUSTPAY_API_KEY
        nounce = self.generate_random_string()
        timestamp = str(int(time.time()))

        message = (
                app_key + nounce + timestamp + str(transaction.amount) + first_name + last_name + email + address + city +
                state + country + phone + return_url + cancel_url + str(transaction.serial_number) +
                str(transaction.id)
        ).replace(" ", "")

        signature = hmac.new(
            key=self.TRUSTPAY_API_SECRET.encode(),
            msg=message.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        payload = {
            "url": base_url + 'callgw',
            "api_key": app_key,
            "nonce": nounce,
            "timestamp": timestamp,
            "amount": str(transaction.amount),
            "signature": signature,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "return_url": return_url,
            "cancel_url": cancel_url,
            "invoice": str(transaction.serial_number),
            "order_id": str(transaction.id),
            "payment_source": phone,
            "payment_network": "MTN",
            "payment_method": "momo",
        }
        print(payload)
        return payload

    def check_pay_success(self, transaction):
        return True
