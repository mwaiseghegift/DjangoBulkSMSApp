from django import forms
from .models import PhoneDb

class phoneVerificationForm(forms.ModelForm):
    model = PhoneDb
    
class ResetEmailForm(forms.Form):
    email = forms.EmailField()