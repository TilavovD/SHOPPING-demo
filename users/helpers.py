import requests
from django.conf import settings
import random
import vonage


def send_secret_code_via_eskiz(phone_number):
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


def send_secret_code_via_vonage(phone_number):
    secret_key = random.randint(100000, 999999)
    client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
    responseData = client.sms.send_message(
        {
            "from": settings.VONAGE_BRAND_NAME,
            "to": phone_number,
            "text": f"Secret code: {secret_key}",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
        return secret_key
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")