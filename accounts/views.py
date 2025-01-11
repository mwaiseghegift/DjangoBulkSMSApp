from django.shortcuts import render, redirect, get_object_or_404, reverse
import random
from django.http import HttpResponse, HttpResponseRedirect
from .models import PhoneDb
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_gen
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .forms import ResetEmailForm
from decouple import config




from django.contrib.auth.models import User

#africanstalking initialization
import africastalking
username = "RETECH-ORG"
api_key = config("API_KEY")
africastalking.initialize(username, api_key)
sms_provider = africastalking.SMS
# Create your views here.


def generateOTP(request):
    number = random.randint(100000,999999)
    print(number)
    return HttpResponse(number)

def LogInView(request, *args, **kwargs):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        if username == "":
            messages.error(request, "Username required")
        if password == "":
            messages.error(request, "Password is required")
        
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            messages.info(request, "You have successfully logged in")
            return redirect('retechecommerce:index')
        else:
            messages.error(request,"Ivalid Login")
            return render(request,'auth/login.html')
    return render(request, 'auth/login.html', {})

def LogOutView(request, *args, **kwargs):
    logout(request)
    messages.success(request,"You have successfully Logged Out")
    return redirect('retechecommerce:index')

def RegisterView(request):
    
    if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            
            if username == "":
                messages.error(request, "Username is required")
            if email == "":
                messages.error(request, "Email is required")
            if password1 == "":
                messages.error(request, "Password is required")
            if password2 == "":
                messages.error(request, "Repeat Password is required")
                return redirect('accounts:register')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "A user with the username exists")
            if User.objects.filter(email=email).exists():
                messages.error(request, "The Email has already been taken")
                return redirect('accounts:register') 
            
            if password1 != password2:
                messages.error(request, "Passwords do not match")
            if len(password1)<6:
                messages.error(request,"Password is too short")
                return redirect('accounts:register') 
              
                    

                    
            else:
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password1)
                user.is_active=False
                user.save()
                
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain #gives us the domain
                link = reverse('accounts:activate', 
                                kwargs={
                                    'uidb64':uidb64, 
                                    'token':token_gen.make_token(user)
                                        })
                activate_url = f"http://{domain+link}"
                
                mail_subject = "Activate your account"
                
                """
                message = render_to_string('auth/activate.html', {
                    'user':user,
                    'domain':domain,
                    'uidb64':uidb64,
                    'token':token_gen.make_token(user)
                })
                """
                
                mail_body = f"hi {user.username} click the link below to verify your account\n {activate_url}"
                mail = send_mail (mail_subject, mail_body,'noreply@retech.com',[email], fail_silently=False)
                messages.success(request, "User has been created")
                return redirect('accounts:login')
            
    return render(request, 'auth/register.html', {})

def VerificationView(request,uidb64, token):

    uidb = force_str(urlsafe_base64_decode(uidb64)) or None
    user = User.objects.get(pk=uidb) or None

        
    if user is not  None and token_gen.check_token(user, token):
        user.is_active=True
        user.save()
        messages.info(request, "account verified")  
        return redirect("accounts:login")
    return render(request,'auth/activation_failed.html')

def RequestResetEmail(request):
    if request.method == 'POST':
        form = ResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
        
    
            user = User.objects.filter(email=email)
        
            if user.exists():
                uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
                domain = get_current_site(request).domain #gives us the domain
                link = reverse('accounts:reset-password', 
                                kwargs={
                                    'uidb64':uidb64, 
                                    'token':PasswordResetTokenGenerator().make_token(user[0])
                                        })
                reset_password_url = f"http://{domain+link}"
                
                mail_subject = "Reset Password"
                
                """
                message = render_to_string('auth/activate.html', {
                    'user':user.username,
                    'url':activate_url,
                })
                """
                
                mail_body = f"hi {user[0].username} click the link below to reset your password\n {reset_password_url}"
                mail = send_mail (mail_subject, mail_body,'noreply@retech.com',[email], fail_silently=False)
                messages.success(request, "Check your Email for the reset link")
                return redirect('accounts:login')
            else:
                messages.error(request, "Sorry, there is no user with that email")
                return redirect('accounts:request-reset-email')

    return render(request, 'auth/reset_email_form.html', {})
  
def ResetPasswordView(request, uidb64, token):
    context = {
        'uidb64':uidb64, 
        'token':token
        }
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.error(request, "Opps, The link has expired")
            return render(request, 'auth/reset_email_form.html', {})
            
        
        messages.success(request, "password changed successfully")
        return redirect('accounts:login')
    except DjangoUnicodeDecodeError as identifier:
        messages.error(request, "oops! something went wrong")
        return render(request, 'auth/reset_password.html', context)
    
    
    if request.method == 'POST':
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == "":
            messages.error(request, "Password is required")
        if password2 == "":
            messages.error(request, "Repeat Password is required")
            return render(request, 'auth/reset_password.html', context)
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return render(request, 'auth/reset_password.html', context)
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        if len(password1)<6:
            messages.error(request,"Password is too short")
            return render(request, 'auth/reset_password.html', context)  
        
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.success(request, "password changed successfully")
            return redirect('accounts:login')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "oops! something went wrong")
            return render(request, 'auth/reset_password.html', context)
    return render(request, 'auth/reset_password.html', context)






def request_otp(request):
    if request.method == 'POST':
        phone_no = request.POST['phone-no']
        
        phone_number = PhoneDb.objects.filter(phone=phone_no)
        if phone_number.exists():
            messages.error(request, "the phone number already exists")
            return HttpResponse(reverse('accounts:request-otp'))
        
        otp = random.randint(100000, 999999)
        otp_model = PhoneDb(
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
        
        user_otp = get_object_or_404(PhoneDb, user=request.user)
        
        if str(entered_otp)==str(user_otp.otp):
            user_otp.is_confirmed=True
            user_otp.save()
            return HttpResponseRedirect(reverse("sms:home"))
        
    return render(request, 'enter-otp.html')
