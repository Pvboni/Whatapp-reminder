import os
from twilio.rest import Client

# Retrieve Twilio Account SID and Auth Token from environment variables
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

# Verify if account_sid and auth_token are retrieved successfully
if account_sid is None or auth_token is None:
    print("Twilio credentials not found. Please set the environment variables TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.")
    exit(1)

client = Client(account_sid, auth_token)

# Send a message
message = client.messages.create(
    body='join skin-sad',
    from_='whatsapp:+14155238886',  # Twilio sandbox number
    to='whatsapp:+5511998995650'  # Your WhatsApp number
)

print(message.sid)
