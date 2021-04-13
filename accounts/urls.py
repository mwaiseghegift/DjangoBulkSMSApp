from django.urls import path
from .views import generateOTP, enter_otp, request_otp

app_name = "accounts"

urlpatterns = [
    path('get-otp/', generateOTP, name="get-otp"),
    path('request-otp/', request_otp, name='request-otp'),
    path('enter-otp/', enter_otp, name="enter-otp"),
]