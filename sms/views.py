from django.shortcuts import render, HttpResponse
import africastalking
from decouple import config
# Create your views here.

username = "sandbox"
api_key = config("api_key")
africastalking.initialize(username, api_key)

# Initialize a service e.g. SMS
sms = africastalking.SMS

def Test_Send(request):
    sms = sms
    sender_id = "RETECH"
    content = "This is the message"
    recepients = ["254712860997"]
    response = sms.send(content, recepients, sender_id)
    return HttpResponse(response)