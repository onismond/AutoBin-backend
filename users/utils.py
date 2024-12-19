from django.contrib.auth import get_user_model
from django.conf import settings
import requests
import random
import re


def is_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    return False


def create_verification_code():
    return str(random.randint(1000, 9999))


def format_contact(contact):
    return f'+233{contact[1:]}'


def format_contact_no_plus(contact):
    return f'233{contact[1:]}'


def send_phone_verification_code(user):
    code = create_verification_code()
    base_url = "https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "key": settings.NALO_AUTH_KEY[0],
        "msisdn": format_contact_no_plus(user.contact),
        "message": f"Your AutoBin OTP is {code}",
        "sender_id": "AutoBin",
    }
    response = requests.post(base_url, headers=headers, json=payload)
    print(response.json())
    user.phone_verification_code = code
    user.save()
    if response.status_code == 200:
        return True
    else:
        return False


def verify_phone_code(user, code):
    if user.phone_verification_code == code:
        return True
    return False


def send_password_change_verification_code(user):
    code = create_verification_code()
    base_url = "https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "key": settings.NALO_AUTH_KEY[0],
        "msisdn": format_contact_no_plus(user.contact),
        "message": f"Your AutoBin OTP is {code}",
        "sender_id": "AutoBin",
    }
    response = requests.post(base_url, headers=headers, json=payload)
    # print(response.json())
    user.password_change_verification_code = code
    user.save()
    if response.status_code == 200:
        return True
    else:
        return False


def verify_password_change_code(user, code):
    if user.password_change_verification_code == code:
        return True
    return False
