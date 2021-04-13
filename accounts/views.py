from django.shortcuts import render, get_object_or_404, reverse
import random
from django.http import HttpResponse, HttpResponseRedirect
from .models import phoneOTP
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decouple import config

#africanstalking initialization
import africastalking
username = "RETECH-ORG"
api_key = config("api_key")
africastalking.initialize(username, api_key)
sms_provider = africastalking.SMS
# Create your views here.


def generateOTP(request):
    number = random.randint(100000,999999)
    print(number)
    return HttpResponse(number)


def request_otp(request):
    if request.method == 'POST':
        phone_no = request.POST['phone-no']
        
        phone_number = phoneOTP.objects.filter(phone=phone_no)
        if phone_number.exists():
            messages.error(request, "the phone number already exists")
            return HttpResponse(reverse('accounts:request-otp'))
        
        otp = random.randint(100000, 999999)
        otp_model = phoneOTP(
            user = request.user,
            phone = phone_no,
            otp = otp,    
        )
        otp_model.save()
        sms = sms_provider
        sender_id = "RETECH"
        sms_content = f"Your phone verification code is {otp}"
        recipients = [str(phone_no)]
        response = sms.send(sms_content, recipients)
        return HttpResponseRedirect(reverse('accounts:enter-otp'))
    return render(request, "enter-phone.html",{})


@login_required
def enter_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['user-otp']
        
        user_otp = get_object_or_404(phoneOTP, user=request.user)
        
        if str(entered_otp)==str(user_otp.otp):
            user_otp.is_confirmed=True
            user_otp.save()
            return HttpResponseRedirect(reverse("sms:home"))
        
    return render(request, 'enter-otp.html')