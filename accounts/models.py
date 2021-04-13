from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()




class PhoneDb(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, default="+254")
    otp = models.IntegerField(null=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{str(self.phone)} - {self.user.username}"
    
        

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    slug = models.SlugField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)