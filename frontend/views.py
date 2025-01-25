from django.shortcuts import render, redirect
from django.shortcuts import  get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now
import datetime
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.timezone import now

from frontend.models import User, Appointment
from django.conf import settings
from django.views import View
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import AppointmentForm , BillingDetailsForm , OrderForm , UserRegistrationForm  , ContactUs
from .models import Document , NewsletterSubscriber
from dashboard.models import Service, Cart, Home, Professional_Services, Hr_Solutions, Government, About_Us, FAQSection
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.http import JsonResponse
from .models import NewsletterSubscriber, Order
from django.template import Context
import zipfile
import os
from django.http import HttpResponse
from io import BytesIO

from .signals import sendEmail


def home(request):

    home_list = Home.objects.all()
    return render(request, 'index.html', {'home_list': home_list})



def about(request):
    about_us = About_Us.objects.all()
    return render(request, 'about-us.html', {'about_us': about_us})




def apostilleservices(request):
    return render(request, 'apostille-services.html') 


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank-you')
        else:
            email_errors = form.errors.get('email', [])
            if email_errors:
                specific_email_error = email_errors[0]  
            else:
                specific_email_error = None
            return render(request, 'appoinment.html', {'form': form, 'specific_email_error': specific_email_error})
    else:
        form = AppointmentForm()

    return render(request, 'appoinment.html', {'form': form})


def backgroundcheck(request):
    return render(request, 'background-check.html') 

def checkout(request, order_id=None):

    if request.method == "POST":
        form = BillingDetailsForm(request.POST)
        if form.is_valid():
            billing_details = form.save(commit=False)
            billing_details.user = request.user
            billing_details.save()
            messages.success(request, 'Your billing details have been saved successfully!')
            return HttpResponseRedirect(reverse('thank-you'))
        else:
            messages.error(request, 'There were errors with your submission.')
    else:
        form = BillingDetailsForm()

    return render(request, 'checkout.html', {
        # 'order': order,
    })

def contact(request):
    if request.method == 'POST':
        form = ContactUs(request.POST)
        if form.is_valid():
            contact_message = form.save()

            subject = 'New Contact Us Submission'
            message = (
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n"
                f"Phone: {contact_message.phone}\n"
                f"Address: {contact_message.address}\n"
                f"Message: {contact_message.comments}"
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.DEFAULT_FROM_EMAIL]

            try:
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')

            return redirect('thank-you')
        else:
            error_messages = form.errors.as_data()
            context_errors = {}
            for field, errors in error_messages.items():
              
                clean_errors = [error.message for error in errors]
              
                context_errors[field] = [err.replace("['", "").replace("']", "") for err in clean_errors]
            
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'contact-us.html', {'form': form, 'errors': context_errors})

    else:
        form = ContactUs()

    return render(request, 'contact-us.html', {'form': form})


@csrf_exempt
def newsletter_submission(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            try:
                subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
                if not created:
                    return JsonResponse({"message": "You are already subscribed.", "status": "error"})

                htmly = get_template('email-template/subscribe-mail.html')
                html_content = htmly.render({"email": email})

             
                plaintext = get_template('email-template/mail.txt')
                plain_content = plaintext.render({"email": email})


                msg = EmailMultiAlternatives(
                    subject="Thank You for Subscribing to Our Newsletter!",
                    body=plain_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return JsonResponse({"message": "Thank you for subscribing!", "status": "success"})
            except Exception as e:
                return JsonResponse({"message": f"Error: {str(e)}", "status": "error"})
        else:
            return JsonResponse({"message": "Invalid email address.", "status": "error"})
    return JsonResponse({"message": "Invalid request method.", "status": "error"})



def cart(request, order_id):
    document_id = order_id
    if not document_id:
        return render(request, 'cart.html', {'error': 'No document ID provided.'})

    document = get_object_or_404(Document, unique_id=document_id)
    order = document.order

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return render(request, 'cart.html', {'error': 'No cart items found for this order.'})

    total_price = sum(cart.service.price * cart.quantity for cart in cart_items)
    total_quantity = sum(cart.quantity for cart in cart_items)

    return render(request, 'cart.html', {
        'order': order,
        'document': document,
        'services': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    })


# @login_required
# def remove_cart_item(request, item_id):
#     cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
#     cart_item.delete()
#     return redirect('cart_with_order', order_id=cart_item.order.unique_id)


def documenttranslationservice(request):
    
    return render(request, 'document-translation-service.html') 

def faqs(request):
    sections = FAQSection.objects.prefetch_related('faqs')
    return render(request, 'faqs.html', {'sections': sections})
    return render(request, 'faqs.html') 

def fingerprintingservice(request):
    return render(request, 'fingerprinting-service.html') 

def government(request):
    government = Government.objects.all()
    return render(request, 'government.html', {'government': government})



def header(request):
    return render(request, 'header.html') 

def hrsolutions(request):
    hr_solution = Hr_Solutions.objects.all()
    return render(request, 'hr-solutions.html', {'hr_solution': hr_solution})


def notarypublicservice(request):
    return render(request, 'notary-public-service.html') 

def privacypolicy(request):
    return render(request, 'privacy-policy.html') 

def professional_services(request):
    professional_services = Professional_Services.objects.all()
    return render(request, 'professional-services.html', {'professional_services': professional_services})


@login_required(login_url='signin')
def placeorder(request):
    if request.method == 'POST':
        USER = request.user
        order_form = OrderForm(request.POST)
        files = request.FILES.getlist('upload_documents')
        types = request.POST.getlist('type')

        if order_form.is_valid() and files and types:
            category_price = order_form.cleaned_data['category_price']

            order = order_form.save(commit=False)
            order.user = request.user 
            order.price = category_price  
            order.save()
            
            for i in range(len(files)):
                document = Document(
                    user=request.user, 
                    order=order, 
                    upload_documents=files[i], 
                    type=types[i] if i < len(types) else None
                )
                document.save()

            selected_services = request.POST.getlist('categoriesList')  
            for service_id in selected_services:
                service = Service.objects.get(id=service_id)
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
                    service=service,
                    defaults={'quantity': 1, 'service_name': service.name, 'service_price': service.price}
                )
                
                if not created:
                    # If the cart item already exists, increase the quantity
                    cart_item.quantity += 1
                    cart_item.save()
            
            messages.success(request, 'Order and documents uploaded successfully.')
            card_data = Cart.objects.all()
            for cart in card_data:
                print("cart -------- : ", cart)

            # Redirect to cart with unique order ID
            # return redirect('cart_with_uuid', order_id=str(order.id))
            return redirect('cart_with_uuid', order_id=str(document.unique_id))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        order_form = OrderForm()
        services = Service.objects.all()

    return render(request, 'place-order.html', {
        'order_form': order_form,
        'services': services  
    })



def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
      
            user = form.save()
            username = user.first_name
            email = user.email
            d = {'username': username}

            plaintext = get_template('email-template/mail.txt')
            htmly = get_template('email-template/welcome-mail.html')

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            
            msg = EmailMultiAlternatives(
                subject="Welcome to Our Platform",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            messages.success(request, "User created successfully!")
            return redirect('welcome')
        else:

            password_errors = form.errors.get('password', [])
            email_errors = form.errors.get('email', [])
            print("email_errors : ", email_errors)
            phone_number_errors = form.errors.get('phone_number', [])
            print("phone_number_errors : ", phone_number_errors)
            context = {
                'form': form,
                'password_errors': password_errors,
                'email_errors': email_errors,
                'phone_number_errors': phone_number_errors
            }
       
            return render(request, 'sign-up.html', context)
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

            if user.is_staff or user.is_superuser:  
                return redirect('/dashboard/')
            else:
                return redirect('professional-services') 
        else:
            messages.error(request, "Invalid credentials. Please try again.")
            return redirect('signin')

    return render(request, 'sign-in.html')

def logout_view(request):
    logout(request) 
    return redirect('/')

def forgetpassword(request):
    context = {}
    if request.method == "POST":
        email = request.POST.get('email')

        if not email:
            context['message'] = "Enter a valid email address."
        else:
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(str(user.pk).encode('utf-8')) 
   
                reset_url = request.build_absolute_uri(
                    reverse('confirm-password', kwargs={'uidb64': uid, 'token': token})
                )
                
                htmly = get_template('email-template/forget-mail.html')
                html_content = htmly.render({"reset_url": "reset_url"}) # to-do

             
                plaintext = get_template('email-template/mail.txt')
                plain_content = plaintext.render({"reset_url": "reset-url"})

                msg = EmailMultiAlternatives(
                    subject='Password Reset Request',
                    body=plain_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                )

                msg.attach_alternative(html_content, "text/html")
                msg.send()
                messages.success(request, "Password reset link sent to your email.")
                context['message'] = "Password reset link sent to your email."
            else:
                messages.error(request, "No account found with this email address.")
                context['message'] = "No account found with this email address."

    return render(request, 'forget-password.html', context)


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
    appointment_id_value = request.GET.get('appointment_id')  # Get the appointment ID from the URL query params
    if appointment_id_value:
        appointment = Appointment.objects.filter(appointment_id=int(appointment_id_value)).first()
        print(appointment)
    else:
        appointment = None
    return render(request, 'thank-you.html', {'appointment': appointment})

def welcome(request):
    return render(request, 'welcome.html') 


def download_order_files(request, id):
    # Get the order and associated files
    order = Order.objects.get(id=id)
    files = order.document_set.all()

    # Create a zip file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for uploaded_file in files:
            file_path = uploaded_file.upload_documents.path
            file_name = os.path.basename(file_path)
            zip_file.write(file_path, arcname=file_name)

    # Prepare the response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename=order_{order.user.first_name}_{order.user.last_name}__files.zip'
    return response


def generate_order_id():
    # Generate a unique order ID using the current timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    order_id = f"ORD-{timestamp}"
    return order_id



def order_cart_notre(request, id):
    id = id
    order_form = OrderForm()
    services = Service.objects.all()
    if request.method == "POST":
        vaye = request.POST
        try:
            # Extract form data
            price = request.POST.get('extraField')
            price = float(price.replace('$', '').strip())
            categoriesList_id = request.POST.get('categoriesList')  # ForeignKey ID for Service (dropdown or select)
             # Price
            pick_date = request.POST.get('pick_date', datetime.date.today())  # Pick date
            pick_time = request.POST.get('pick_time', datetime.datetime.now().time())  # Pick time
            order_status = request.POST.get('order_status', 'Not Started')  # Default value if not provided
            terms_accepted = request.POST.get('terms_accepted') == 'on'  # Checkbox for terms accepted

            # Get the Service object for the given categoriesList_id
            categoriesList = Service.objects.get(id=categoriesList_id)  # Fetch the Service object by ID
            order_id = id
            # Create and save the Order object
            order = Order(
                user=request.user,  # Assuming the logged-in user
                categoriesList=categoriesList,  # Set the ForeignKey field
                price=price,
                pick_date=pick_date,
                pick_time=pick_time,
                order_status=order_status,
                terms_accepted=terms_accepted,
                created_at=now()
            )
            order.save()

            print("Order exists:", order)
            user = request.user
            order = order
            pagename = request.POST.get('name')
            document = request.POST.get('pageNumbers')
            upload_documents = request.FILES.getlist('upload_documents')

            if upload_documents:
                for file in upload_documents:
                    document_instance = Document(
                        user=user,
                        order=order,
                        upload_documents=file,
                        type=pagename,
                        number_of_document=document
                    )
                    document_instance.save()
                    messages.success(request, "Documents uploaded successfully.")
                    if document_instance:
                        sendEmail(too=['m.haneef1966@gmail.com'],
                                  temp=None)
                        return HttpResponse("<h1>Thank you for choosing HR Solution, please check your email for registration completion</h1>")
            else:
                document_instance = Document(
                    user=user,
                    order=order,
                    upload_documents=None,
                    type=pagename,
                    number_of_document=document
                )
                document_instance.save()
                messages.success(request, "Documents uploaded successfully.")
                if document_instance:
                    sendEmail(too=['m.haneef1966@gmail.com'], sub="Thank you for choosing Right HR Solution, please check your email for registration completion",
                                  temp="Your registration is now complete!")
                    return HttpResponse("<h1>Thank you for choosing Right HR Solution, please check your email for registration completion</h1>")
        except Service.DoesNotExist:
            messages.error(request, "The selected service category does not exist.")
            return render(request, 'order_cart_notre.html', {'services': services, 'id': id})

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'order_cart_notre.html', {'services': services, 'id': id})

        else:
            if request.method == "GET":
                pass
    return render(request, 'order_cart_notre.html', {'order_form': order_form, 'services': services, 'id': id})


# def send_email_notification(user):
#     subject = "Welcome to Our Platform"
#     if user.is_superuser:
#         subject = "Superuser Notification: Welcome to Our Platform"
#
#     message = render_to_string("email_template.html", {'user': user})
#
#     # Send email to the user
#     send_mail(
#         subject,
#         message,
#         settings.EMAIL_HOST_USER,
#         [user.email],
#         fail_silently=False
#     )
