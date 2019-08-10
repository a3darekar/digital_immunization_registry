import os

from twilio.rest import Client

account_sid = os.environ['twilio_acc_sid']
# Your Auth Token from twilio.com/console
auth_token = os.environ['twilio_auth_token']

client = Client(account_sid, auth_token)

# 	message = client.messages.create(
#	 	to="+918788957859",
# 		from_="+13373074483",
# 		body="I'm Bored!!"
# 	)

# print repr(message)
# devices = FCMDevice.objects.all()
# print devices
# for device in devices:
# 	body = "Test Message body"
# 	device.send_message(title="Test Messge title", body=body)
