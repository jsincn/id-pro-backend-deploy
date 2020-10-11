# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = os.environ.get("twilio-id-pro-sid")
auth_token = os.environ.get("twilio-id-pro-token")

def send_message(to, id):
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="Ihre ID ist: " + str(id) + " - An einem sicheren Ort aufbewahren! - Privacy: https://stei.ml/privacy - Info: https://stei.ml/info",
        from_="IDPRO",
        to=to
    )

def send_recovery_message(to, id):
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="Ihre ID ist: " + str(id) + " - An einem sicheren Ort aufbewahren! - Privacy: https://stei.ml/privacy - Info: https://stei.ml/info",
        from_="IDPRO",
        to=to
    )

    messages = client.messages.list(limit=20)

    for record in messages:
        if record.sid != message.sid:
            client.messages(record.sid).delete()