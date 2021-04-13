from django.urls import path
from .views import generateOTP

urlpatterns = [
    path('get-otp/', generateOTP, name="get-otp"),
]