import vonage
from django.conf import settings
import random

def send_secret_code(user):
    secret_key = random.randint(100000, 999999)
    client = vonage.Client(key=settings.VONAGE_CLIENT_KEY, secret=settings.VONAGE_SECRET_KEY)
    sms = vonage.Sms(client)
    response = sms.send_message(
        {
            "from": "S-orca",
            "to": f"{user.phone_number}",
            "text": f"Secret key: {secret_key}",
        }
    )

    if response["messages"][0]["status"] == "0":
        print("Message Details: ", response)
        print("Message sent successfully.")
        user.secret_key = secret_key
        user.save()
    else:
        print(f"Message failed with error: {response['messages'][0]['error-text']}")
