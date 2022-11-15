import requests
from django.conf import settings
import random


def send_secret_code(phone_number):
    secret_key = random.randint(100000, 999999)
    url = "https://notify.eskiz.uz/api/message/sms/send"

    payload = {'mobile_phone': f'{phone_number[1:]}',
               'message': f'Maxfiy kod: {secret_key}',
               'from': '4546',
               'callback_url': 'http://0000.uz/test.php'}
    files = [

    ]
    headers = {
        'Authorization': f'Bearer {settings.ESKIZ_SMS_TOKEN}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        return secret_key
    return None
