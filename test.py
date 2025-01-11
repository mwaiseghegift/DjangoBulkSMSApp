# import package
import africastalking
from decouple import config


# Initialize SDK
username = "bulk-sms-steve"    # use 'sandbox' for development in the test environment
api_key = config("API_KEY")      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
response = sms.send("Hello Message!", ["+256758969973"])
print(response)

# Or use it asynchronously
def on_finish(error, response):
    if error is not None:
        raise error
    print(response)

sms.send("Hello Message!", ["+256758969973"], callback=on_finish)    
