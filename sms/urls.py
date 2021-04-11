from .views import *
from django.urls import path

app_name = "sms"

urlpatterns = [
    path('', Index, name="home"),
    path('send/', Send_Text, name='send'),
]