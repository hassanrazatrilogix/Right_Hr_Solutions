from django.shortcuts import render, redirect
from django.shortcuts import  get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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
            return redirect('cart')
    else:
        form = AppointmentForm()

    return render(request, 'appoinment.html', {'form': form})

def backgroundcheck(request):
    return render(request, 'background-check.html') 

def checkout(request):
    return render(request, 'checkout.html') 

def contactus(request):
    return render(request, 'contact-us.html') 

def cart(request,order_id):
    document_id = order_id
    print("documnet id -------",document_id )
    if not document_id:
        return render(request, 'cart.html', {'error': 'No document ID provided.'})

    document = get_object_or_404(Document, unique_id=document_id)
    order = document.order

    return render(request, 'cart.html', {
        'order': order,
        'document': document,
    })

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

@login_required(login_url='signin')
def placeorder(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST) 
        files = request.FILES.getlist('upload_documents')
        types = request.POST.getlist('type')
          
        if order_form.is_valid() and files and types:
            category_price = order_form.cleaned_data['category_price']

            order = order_form.save()
            order.price = category_price 
            order.save()
            
            for i in range(len(files)):
                document = Document(user=request.user, order=order, upload_documents=files[i], type=types[i] if i < len(types) else None)
                document.save()
            
            messages.success(request, 'Order and documents uploaded successfully.')

            return redirect('cart_with_uuid', order_id=str(document.unique_id))
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
        email = request.POST.get('email')

        user = User.objects.filter(email=email).first()  

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8')) 
            
            reset_url = request.build_absolute_uri(
                reverse('confirmpassword', kwargs={'uidb64': uid, 'token': token})
            )
            
            subject = 'Password Reset Request'
            
            message = render_to_string('password_reset_email.html', {'reset_url': reset_url})
            
            send_mail(subject, message, 'pythonweb@exoticaitsolutions.com', [email])
            messages.success(request, "Password reset link sent to your email.")
        else:
            messages.error(request, "No account found with this email address.")
        
        return redirect('forgetpassword')

    return render(request, 'forget-password.html')



def confirmpassword(request, uidb64, token):
 
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        print(f"Decoded UID: {uid}")

        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            print("Token is valid.")
            if request.method == "POST":
            
                new_password = request.POST.get('new-password')
                confirm_password = request.POST.get('confirm-password')

                if new_password == confirm_password:
                    print("Passwords match. Setting new password.")
                   
                    user.set_password(new_password)
                    user.save()
    
                    user = User.objects.get(pk=user.pk)

                    user_authenticated = authenticate(email=user.email, password=new_password)
                    if user_authenticated is not None:
                        login(request, user_authenticated)  
                        print("User re-authenticated and logged in.")

                        messages.success(request, "Your password has been reset successfully. Please sign in.")
                        return redirect('signin')
                    else:
                        print("Authentication failed after password reset.")
                        messages.error(request, "Authentication failed after password reset.")
                else:
                    messages.error(request, "Passwords do not match.")
                    print("Passwords do not match.")
            return render(request, 'confirm-password.html')
        else:
            return HttpResponse('Invalid or expired link', status=400)
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
 
        print(f"Error during password reset: {str(e)}")
        return HttpResponse('Invalid link', status=400)



def termsconditions(request):
    return render(request, 'terms-conditions.html') 

def thankyou(request):
    return render(request, 'thank-you.html') 