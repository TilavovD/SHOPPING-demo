import os
import vonage


#Create a client instance and then pass the client to the Sms instance
client = vonage.Client(key="81402ff2", secret="N7jaAyMcoV9JjByT")
sms = vonage.Sms(client)
response = sms.send_message(
    {
        "from": "S-orca",
        "to": "+998994400138",
        "text": "Assalomu alaykum. Bu test SMS",
    }
)

if response["messages"][0]["status"] == "0":
    print("Message Details: ", response)
    print("Message sent successfully.")
else:
    print(f"Message failed with error: {response['messages'][0]['error-text']}")