from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()

class phoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be in the format 254712345678")
    phone  = models.CharField(validators=[phone_regex], max_length=12, unique=True)
    otp = models.CharField(max_length=10, blank=True, null=True)
    count = models.IntegerField(default=0, help_text="OTP sent")
    validated = models.BooleanField(default=False, help_text="if true, the phone is validated")
    otp_session_id = models.CharField(max_length = 120, null=True, default="")
    username = models.CharField(max_length=255, blank=True, null=True, default=None)
    email = models.CharField(max_length=255, blank=True, null=True, default=None)
    password = models.CharField(max_length=255, blank=True, null=True, default=None)
    
    def __str__(self):
        return f"{str(self.phone)} has been sent {str(self.otp)}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)