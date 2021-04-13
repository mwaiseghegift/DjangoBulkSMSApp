from django.shortcuts import render
import random
from django.http import HttpResponse, HttpResponseRedirect
from .models import phoneOTP
# Create your views here.


def generateOTP(request):
    number = random.randint(100000,999999)
    print(number)
    return HttpResponse(number)


def request_otp(request):
    if request.method == 'POST':
        phone_no = request.POST['phone']
        
        if phone_no.is_valid:
            otp = random.randint(100000, 999999)
            otp_model = phoneOTP(
                user = request.user,
                phone = phone_no,
                otp = otp,    
            )
            otp_model.save()
            return HttpResponseRedirect()
    return render(request, "enter-phone.html",())