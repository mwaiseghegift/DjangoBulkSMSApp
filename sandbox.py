import os
import africastalking
from decouple import config

username ="sandbox"
api_key = config("api_key")
africastalking.initialize(username, api_key)

sms = africastalking.SMS
response = sms.send("This is Gift Testing", ["+254712860997"],"RETECH")
print(response)


