from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

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

def forgetpassword(request):
    return render(request, 'forget-password.html') 

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
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save()
            print(order)  
            return redirect('thankyou')
        else:
            print("Form errors:", form.errors)  
    else:
        form = OrderForm()

    return render(request, 'place-order.html', {'form': form})


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


def termsconditions(request):
    return render(request, 'terms-conditions.html') 

def thankyou(request):
    return render(request, 'thank-you.html') 