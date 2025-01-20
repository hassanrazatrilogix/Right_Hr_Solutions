from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from datetime import datetime

from django.utils import timezone

from frontend.forms import ServiceForm, ServiceTypeForm, HomeForm, ProfessionalServicesForm, HRSolutionsForm, \
    GovernmentForm, AboutUsForm, HelpForm, FAQForm, FAQSectionForm, AppointmentForm
from dashboard.models import Service, ServiceType, Cart, Home, Professional_Services, Hr_Solutions, Government, About_Us, Help, FAQ, FAQSection
from frontend.models import Order, User, Appointment
from django.shortcuts import  get_object_or_404
from frontend.forms import UserEditForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncDay, TruncYear, TruncMonth
import json
from django.contrib.auth.hashers import make_password


@login_required(login_url='signin')
def dashboard_summary(request):
    query = request.GET.get('q', '')
    thirty_days_ago = now() - timedelta(days=30)
    current_year = timezone.now().year
    if request.user.is_superuser:
        orders = Order.objects.filter(created_at__gte=thirty_days_ago)
    else:
        orders = Order.objects.filter(user=request.user, created_at__gte=thirty_days_ago)

    # Statistics for cards
    total_orders = orders.count()
    total_users = User.objects.count()
    latest_users = User.objects.order_by('-id')[:10]
    total_revenue = orders.aggregate(total_revenue=Sum('price'))['total_revenue'] or 0
    yearly_revenue = orders.filter(created_at__year=current_year).aggregate(total_revenue=Sum('price'))[
                        'total_revenue'] or 0

    # Aggregate total price by day for the chart
    orders_by_month = (
        orders.annotate(month=TruncMonth('created_at'))  # Grouping by year instead of day
        .values('month')
        .annotate(total_price=Sum('price'))
        .order_by('month')
    )

    bar_chart_data = {
        'labels': [entry['month'].strftime('%Y') for entry in orders_by_month],  # Show year in the label
        'data': [float(entry['total_price']) if entry['total_price'] else 0 for entry in orders_by_month],
    }

    return render(
        request,
        'summary.html',
        {
            'orders': orders[:5],
            'total_orders': total_orders,
            'latest_users': latest_users,
            'total_users': total_users,
            'total_revenue': total_revenue,
            'yearly_revenue': yearly_revenue,
            'bar_chart_json': json.dumps(bar_chart_data),
        }
    )

@login_required(login_url='signin')
def all_orders(request):
    x = '000'
    query = request.GET.get('q', '')  
    if request.user.is_superuser:
        orders = Order.objects.prefetch_related('document_set').all()
    else:
        orders = Order.objects.prefetch_related('document_set').filter(user=request.user)

    if query: 
        orders = orders.filter(
            Q(user__email__icontains=query) |  
            Q(id__icontains=query)          
        )

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    orders_page = paginator.get_page(page_number)
        
    return render(request, 'home.html', {'orders': orders_page, 'x': x})


@login_required(login_url='signin')
def edit_orders(request, id):
    query = request.GET.get('q', '')
    if request.user.is_superuser:
        edit_orders = get_object_or_404(Order, id=id)
        print(edit_orders)
    else:
        edit_orders = get_object_or_404(Order, id=id)
        print(edit_orders)
    if request.method == "POST":
        pick_date_str = request.POST.get('pick_date')
        pick_time_str = request.POST.get('pick_time')
        pick_time_str = pick_time_str.replace('.', '').upper()
        try:
            pick_time = datetime.strptime(pick_time_str, "%I:%M %p").time()  # Format: '11:05 a.m.'
        except ValueError:
            raise ValueError("Invalid time format. Expected format is HH:MM AM/PM.")
        try:
            pick_date = datetime.strptime(pick_date_str, "%b. %d, %Y").date()  # Format: 'Jan. 7, 2025'
        except ValueError:
            raise ValueError("Invalid date format. Expected format is YYYY-MM-DD.")
        res = Order.update(id,
                           request.POST.get('name'),
                           request.POST.get('service'),
                           request.POST.get('price'),
                           pick_date,
                           pick_time,
                           request.POST.get('order_status'),
                           request.POST.get('term_acc'),
                           )
        print(res)
        return redirect('orders')
    return render(request, 'edit_orders.html', {'edit_orders': edit_orders})


@login_required(login_url='signin')
def user(request):
        x = '000'
        User = get_user_model()

        if not request.user.is_superuser:
            users = [request.user] 
        else:
            users = User.objects.all() 
             
        search_query = request.GET.get('q', '').strip()  
        if search_query:
            users = users.filter(
                Q(first_name__icontains=search_query) | 
                Q(email__icontains=search_query)
            )

        paginator = Paginator(users, 5) 
        page_number = request.GET.get('page')
        users_page = paginator.get_page(page_number)

        if request.method == 'POST' and request.user.is_superuser:
            user_id = request.POST.get('user_id')
            action = request.POST.get('action')  
            try:
                user_to_update = User.objects.get(id=user_id)
                if action == 'promote':
                    user_to_update.is_superuser = True
                elif action == 'demote':
                    user_to_update.is_superuser = False
                user_to_update.save()
            except User.DoesNotExist:
                pass 

            return redirect('user')  

        return render(request, 'user.html', {'users': users_page, 'x': x})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if not request.user.is_superuser:
        return redirect('user')  # Redirect if not a superuser

    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)

            # Handle password change
            password = form.cleaned_data.get('password')
            if password:
                user.password = make_password(password)  # Hash the new password

            user.save()
            return redirect('user')  # Redirect after successful update
    else:
        form = UserEditForm(instance=user)

    return render(request, 'edit-user.html', {'form': form, 'user': user})

# Service - CRUD
@login_required(login_url='signin')
def service_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    services = Service.objects.all()
    return render(request, 'service-list.html', {'services': services})

@login_required(login_url='signin')
def service_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'service-form.html', {'form': form})

@login_required(login_url='signin')
def service_update(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service-form.html', {'form': form})

@login_required(login_url='signin')
def service_delete(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'service-confirm-delete.html', {'service': service})

#  ServiceType - CURD

@login_required
def service_type_list(request):
    service_types = ServiceType.objects.all()
    return render(request, 'service-type-list.html', {'service_types': service_types})

@login_required
def service_type_create(request):
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_type_list')
    else:
        form = ServiceTypeForm()
    return render(request, 'service-type-form.html', {'form': form})


@login_required
def service_type_edit(request, pk):
    service_type = get_object_or_404(ServiceType, pk=pk)
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, instance=service_type)
        if form.is_valid():
            form.save()
            return redirect('service_type_list')
    else:
        form = ServiceTypeForm(instance=service_type)
    return render(request, 'service-type-form.html', {'form': form})


@login_required
def service_type_delete(request, pk):
    service_type = get_object_or_404(ServiceType, pk=pk)
    if request.method == 'POST':
        service_type.delete()
        return redirect('service_type_list')
    return render(request, 'service-type-confirm-delete.html', {'service_type': service_type})




@login_required
def add_to_cart(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, service=service)
    if not created:
        cart_item.quantity += 1  
        cart_item.save()
    return redirect("view_cart")

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.service.price * item.quantity for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def remove_from_cart(request, service_id):
    cart_item = get_object_or_404(Cart, user=request.user, service_id=service_id)
    cart_item.delete()
    return redirect("view_cart")

#To Do
@login_required
def home_list(request):
    home_data = Home.objects.all()
    hr_solutions = Hr_Solutions.objects.all()
    professional_services = Professional_Services.objects.all()
    government = Government.objects.all()
    about_us = About_Us.objects.all()
    all_pages = list(home_data) + list(hr_solutions) + list(professional_services) + list(government) + list(about_us)

    return render(request, 'pages.html', {'all_pages': all_pages})

from django.http import HttpResponse

def reset_to_original_view(request, model_name, model_id):
    if request.method == "GET":
        # Dynamically get the model class
        model_class = {'home': Home, 'Professional_Services': Professional_Services, 'Hr_Solutions': Hr_Solutions, "Government":Government, 'About_Us': About_Us, 'FAQSection':FAQSection}.get(model_name.lower())
        if not model_class:
            return HttpResponse("Invalid model name.", status=400)

        instance = get_object_or_404(model_class, id=model_id)
        instance.reset_to_original()
        return redirect('/dashboard/home_list')
    return redirect('/dashboard/home_list')
    

@login_required
def home_edit(request, home_id):
    home_instance = get_object_or_404(Home, pk=home_id)

    if request.method == 'POST':
        form = HomeForm(request.POST, request.FILES, instance=home_instance)

        if form.is_valid():
            form.save()
            return redirect('home_list')
        else:
            return render(request, "dashboard/page-edit.html", {'home_instance': home_instance, 'form': form})

    else:
        form = HomeForm(instance=home_instance)

    return render(request, "dashboard/page-edit.html", {'home_instance': home_instance, 'form': form})

@login_required
def edit_professional_services(request, professional_id):
    professional_service = get_object_or_404(Professional_Services, id=professional_id)

    if request.method == 'POST':
        form = ProfessionalServicesForm(request.POST, request.FILES, instance=professional_service)
        if form.is_valid():
            form.save()
            return redirect('home_list')
    else:
        form = ProfessionalServicesForm(instance=professional_service)

    return render(request, 'edit_professional_services.html', {'form': form, 'professional_service': professional_service})

@login_required
def edit_hr_solutions(request, hr_solution_id):
    # Fetch the existing Hr_Solutions instance by primary key (pk)
    hr_solution = get_object_or_404(Hr_Solutions, pk=hr_solution_id)

    if request.method == 'POST':
        # Create a form instance with POST data and any files (e.g., images)
        form = HRSolutionsForm(request.POST, request.FILES, instance=hr_solution)

        if form.is_valid():
            form.save()  # Save the updated instance to the database
            return redirect('home_list')  # Redirect to a success page or another page after saving
    else:
        # Initialize the form with the existing data
        form = HRSolutionsForm(instance=hr_solution)

    return render(request, 'edit_hr_solutions.html', {'form': form, 'hr_solution': hr_solution})

@login_required
def edit_government(request, government_id):
    # Fetch the existing Government instance by primary key (pk)
    government = get_object_or_404(Government, pk=government_id)

    if request.method == 'POST':
        # Initialize the form with POST data and any files (images, etc.)
        form = GovernmentForm(request.POST, request.FILES, instance=government)

        if form.is_valid():
            form.save()  # Save the updated instance to the database
            return redirect('home_list')  # Redirect to a success page or another URL
    else:
        # Initialize the form with the current data of the Government instance
        form = GovernmentForm(instance=government)

    return render(request, 'edit_government.html', {'form': form, 'government': government})


@login_required
def edit_about_us(request, about_us_id):
    # Fetch the existing About_Us instance by primary key (pk)
    about_us = get_object_or_404(About_Us, pk=about_us_id)

    if request.method == 'POST':
        # Initialize the form with POST data and any files (for image/file uploads)
        form = AboutUsForm(request.POST, request.FILES, instance=about_us)

        if form.is_valid():
            form.save()  # Save the updated instance to the database
            return redirect('home_list')  # Redirect to a success page (replace with the correct URL)
    else:
        # Initialize the form with the current data of the About_Us instance
        form = AboutUsForm(instance=about_us)

    return render(request, 'edit_about_us.html', {'form': form, 'about_us': about_us})


def help(request):
    
    return render(request, "dashboard/help.html")

# List View
def help_list(request):
    items = Help.objects.all()
    return render(request, 'dashboard/help.html', {'items': items})

# Add View
def help_add(request):
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('help_list')
    else:
        form = HelpForm()
    return render(request, 'add_help.html', {'form': form, 'action': 'Add'})

# Edit View
def help_edit(request, pk):
    item = get_object_or_404(Help, pk=pk)
    if request.method == 'POST':
        form = HelpForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('help_list')
    else:
        form = HelpForm(instance=item)
    return render(request, 'add_help.html', {'form': form, 'action': 'Edit'})

# Delete View
def help_delete(request, pk):
    item = get_object_or_404(Help, pk=pk)
    if request.method == 'GET':
        item.delete()
        return redirect('help_list')
    return render(request, 'help_confirm_delete.html', {'item': item})




@login_required(login_url='signin')
def faq_section_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    sections = FAQSection.objects.all()
    return render(request, 'faq-section-list.html', {'faq_sections': sections})


@login_required(login_url='signin')
def faq_section_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    if request.method == 'POST':
        form = FAQSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq_section_list')
    else:
        form = FAQSectionForm()
    return render(request, 'faq-section-form.html', {'form': form})


@login_required(login_url='signin')
def faq_section_update(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    section = get_object_or_404(FAQSection, pk=pk)
    if request.method == 'POST':
        form = FAQSectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            return redirect('faq_section_list')
    else:
        form = FAQSectionForm(instance=section)
    return render(request, 'faq-section-form.html', {'form': form})


@login_required(login_url='signin')
def faq_section_delete(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    section = get_object_or_404(FAQSection, pk=pk)
    if request.method == 'GET':
        section.delete()
        return redirect('faq_section_list')
    return render(request, 'faq-section-confirm-delete.html', {'section': section})


# FAQ - CRUD
@login_required(login_url='signin')
def faq_list(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    faqs = FAQ.objects.select_related('section').all()
    return render(request, 'faq-list.html', {'faqs': faqs})


@login_required(login_url='signin')
def faq_create(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq_list')
    else:
        form = FAQForm()
    return render(request, 'faq-form.html', {'form': form})


@login_required(login_url='signin')
def faq_update(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect('faq_list')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'faq-form.html', {'form': form})


@login_required(login_url='signin')
def faq_delete(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden("You do not have permission to access this page.")
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'GET':
        faq.delete()
        return redirect('faq_list')
    return render(request, 'faq-confirm-delete.html', {'faq': faq})



@login_required(login_url='signin')
def appointment_list(request):
    appointment_list = Appointment.objects.all()
    paginator = Paginator(appointment_list, 10)
    page_number = request.GET.get('page')
    appointment_page = paginator.get_page(page_number)
    return render(request ,'dashboard/appointment_list.html', {'appointment_page': appointment_page})


@login_required(login_url='signin')
def edit_appointment_list(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'edit_appointment.html', {'form': form, 'appointment': appointment})








