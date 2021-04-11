from django.shortcuts import render, HttpResponse
import africastalking
from decouple import config
# Create your views here.

username = "RETECH-ORG"
api_key = config("api_key")
africastalking.initialize(username, api_key)

# Initialize a service e.g. SMS
sms_afr = africastalking.SMS

def Index(request):
    return render(request, 'index.html', {})

def Send_Text(request):
    if request.method == "POST":
        sms_content = request.POST['message']
        sms = sms_afr
        sender_id = "RETECH"
        content = sms_content
        recepients = ["+254729754363","+254712860997"]
        response = sms.send(content, recepients)
        return HttpResponse(dict(response))