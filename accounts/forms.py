from django import forms
from .models import phoneOTP

class phoneVerificationForm(forms.ModelForm):
    model = phoneOTP