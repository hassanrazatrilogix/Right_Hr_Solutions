from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.forms import modelformset_factory
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import *
from .models import *

def home(request):
    return render(request, 'index.html')  

def about(request):
    return render(request, 'about-us.html') 

def apostilleservices(request):
    return render(request, 'apostille-services.html') 


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thankyou')
    else:
        form = AppointmentForm()

    return render(request, 'appoinment.html', {'form': form})

def backgroundcheck(request):
    return render(request, 'background-check.html') 

def checkout(request):
    return render(request, 'checkout.html') 

def contactus(request):
    return render(request, 'contact-us.html') 

def documenttranslationservice(request):
    return render(request, 'document-translation-service.html') 

def faqs(request):
    return render(request, 'faqs.html') 

def fingerprintingservice(request):
    return render(request, 'fingerprinting-service.html') 

def government(request):
    return render(request, 'government.html') 

def header(request):
    return render(request, 'header.html') 

def hrsolutions(request):
    return render(request, 'hr-solutions.html') 

def notarypublicservice(request):
    return render(request, 'notary-public-service.html') 

def privacypolicy(request):
    return render(request, 'privacy-policy.html') 

def professional_services(request):
    return render(request, 'professional-services.html') 


def placeorder(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        
        files = request.FILES.getlist('upload_documents')
        types = request.POST.getlist('type')
         
        if order_form.is_valid() and files and types:
      
            order = order_form.save()
            
            for i in range(len(files)):
         
                document = Document(order=order, upload_documents=files[i], type=types[i] if i < len(types) else None)
                document.save()
            
            messages.success(request, 'Order and documents uploaded successfully.')
            return redirect('thankyou')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        order_form = OrderForm()

    return render(request, 'place-order.html', {
        'order_form': order_form,
    })



def signup(request):
    if request.method == 'POST': 
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect('signin')
        else:
            print(form.errors)  
    else:
        form = UserRegistrationForm()

    return render(request, 'sign-up.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('thankyou')  
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            print("Invalid credentials. Please try again.")
            return redirect('signin')

    return render(request, 'sign-in.html')


def forgetpassword(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                token = token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode()).decode()
                reset_link = f"{get_current_site(request).domain}/reset/{uid}/{token}/"
                
                subject = "Password Reset Request"
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

                messages.success(request, "Password reset link has been sent to your email.")
                return redirect('forgetpassword')
            except User.DoesNotExist:
                messages.error(request, "Email not registered.")
    else:
        form = PasswordResetForm()

    return render(request, 'forget-password.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Your password has been reset successfully.")
                    return redirect('login') 
            else:
                form = SetPasswordForm(user)
            return render(request, 'password_reset_confirm.html', {'form': form})
        else:
            messages.error(request, "This password reset link is invalid or expired.")
            return redirect('forgetpassword')
    except (User.DoesNotExist, ValueError, TypeError):
        messages.error(request, "Invalid token or user.")
        return redirect('forgetpassword')

def termsconditions(request):
    return render(request, 'terms-conditions.html') 

def thankyou(request):
    return render(request, 'thank-you.html') 