from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.utils.datetime_safe import datetime

from frontend.forms import ServiceForm , ServiceTypeForm
from dashboard.models import Service, ServiceType, Cart, Pages, Add_Section, Content, Sub_Content
from frontend.models import Order, User
from django.shortcuts import  get_object_or_404
from frontend.forms import UserEditForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncDay
import json
from django.contrib.auth.hashers import make_password


@login_required(login_url='signin')
def dashboard_summary(request):
    query = request.GET.get('q', '')
    thirty_days_ago = now() - timedelta(days=30)

    if request.user.is_superuser:
        orders = Order.objects.filter(created_at__gte=thirty_days_ago)
    else:
        orders = Order.objects.filter(user=request.user, created_at__gte=thirty_days_ago)

    # Statistics for cards
    total_orders = orders.count()
    total_users = User.objects.count()
    latest_users = User.objects.order_by('-id')[:5]
    total_revenue = orders.aggregate(total_revenue=Sum('price'))['total_revenue'] or 0

    # Aggregate total price by day for the chart
    orders_by_day = (
        orders.annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(total_price=Sum('price'))
        .order_by('day')
    )

    bar_chart_data = {
        'labels': [entry['day'].strftime('%Y-%m-%d') for entry in orders_by_day],
        'data': [float(entry['total_price']) if entry['total_price'] else 0 for entry in orders_by_day],
    }

    return render(
        request,
        'summary.html',
        {
            'orders': orders,
            'total_orders': total_orders,
            'latest_users': latest_users,
            'total_users': total_users,
            'total_revenue': total_revenue,
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

    paginator = Paginator(orders, 5) 
    page_number = request.GET.get('page')
    orders_page = paginator.get_page(page_number)
        
    return render(request, 'home.html', {'orders': orders_page, 'x': x})


@login_required(login_url='signin')
def edit_orders(request, order_id):
    query = request.GET.get('q', '')
    if request.user.is_superuser:
        edit_orders = get_object_or_404(Order, id=order_id)
        print(edit_orders)
    else:
        edit_orders = get_object_or_404(Order, id=order_id)
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
        res = Order.update(order_id,
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

            # Handle email change
            new_email = form.cleaned_data.get('email')
            if new_email:
                user.email = new_email

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

def pages(request):
    page_data = Pages.objects.all()
    return render(request, "dashboard/pages.html", {"page_data": page_data})

def section_list(request):
    section_list = Add_Section.objects.all()
    return render(request, "dashboard/section-list.html", {'section_list': section_list})

def section_add(request):
    page = Pages.objects.all()
    if request.method == "POST":
        res = Add_Section.add(
            request.POST.get('select_section'),
            request.POST.get('sec_name')
        )
        print("\n\n\nresult\n\n", res)
    return render(request, "dashboard/section-add.html", {'page': page})


def section_edit(request, section_id):
    sec_Edit = get_object_or_404(Add_Section, id=section_id)

    if request.method == "POST":
        res = Add_Section.update(
            section_id,
            request.POST.get('sec_name'),
        )
        print("\n\n\nresult\n\n", res)
    return render(request, "dashboard/section-edit.html", {'sec_Edit': sec_Edit})


def delete_section(request, section_id):
    sec_delete = get_object_or_404(Add_Section, id=section_id)

    sec_delete.delete()

    return redirect('/')


def content_list(request):
    conten_list = Content.objects.all()

    return render(request, "dashboard/content-list.html", {"conten_list": conten_list})


def add_content(request):
    page = Pages.objects.all()
    print(page)
    sections = Add_Section.objects.all()
    print(sections)
    pages_list = list(page.values())
    sections_list = list(sections.values())
    content = Content.objects.all()
    data = {
        'pages': pages_list,
        'sections': sections_list
    }

    if request.method == "POST":
        result = Content.add(
            request.POST.get('Select_Page'),
            request.POST.get('select_section'),
            request.POST.get('content_heading'),
            request.POST.get('content'),
            request.FILES['myfile'],
            request.POST.get('content_button')
        )

        print("\n\n\nresult\n\n", result)
        if result:
            subheading_names = request.POST.getlist('subheading_name')
            subheading_descriptions = request.POST.getlist('subheading_description')
            subheading_images = request.FILES.getlist('subheading_image')
            for i in range(len(subheading_names)):
                res = Sub_Content.add(
                    Content.objects.get(id=result.id),
                    subheading_names[i],
                    subheading_descriptions[i],
                    subheading_images[i] if i < len(subheading_images) else None

                )
                print(res)
    jsonData = json.dumps(data, indent=4)
    return render(request, "dashboard/add-content.html", {'page': page, 'sections': sections, 'jsonData': jsonData, 'content':content})


def edit_content(request, content_id):
    pages = Pages.objects.all()
    sections = Add_Section.objects.all()

    # Get the content to update and its related sub-contents
    content_to_update = get_object_or_404(Content, id=content_id)
    sub_contents = list(Sub_Content.objects.filter(contentHeading=content_to_update.id))  # Convert QuerySet to a list

    # Prepare data for rendering
    pages_list = list(pages.values())
    sections_list = list(sections.values())
    sub_content_list = list(Sub_Content.objects.filter(contentHeading=content_to_update.id).values())  # Serialize sub_contents

    data = {
        'pages': pages_list,
        'sections': sections_list,
        'sub_content': sub_content_list,
    }

    if request.method == 'POST':
        # Update main content fields
        try:
            content_to_update.selectPage = Pages.objects.get(id=request.POST.get('Select_Page'))
            content_to_update.selectSection = Add_Section.objects.get(id=request.POST.get('select_section'))
            content_to_update.contentHeading = request.POST.get('content_heading')
            content_to_update.contentDescription = request.POST.get('content')

            if 'myfile' in request.FILES:
                content_to_update.contentImage = request.FILES.get('myfile', None)

            content_to_update.contentButton = request.POST.get('content_button')
            content_to_update.save()

        except Pages.DoesNotExist:
            print("Error: Selected page does not exist.")
        except Add_Section.DoesNotExist:
            print("Error: Selected section does not exist.")

        # Handle subcontents only if they exist in the POST data
        subheading_names = request.POST.getlist('subheading_name')
        subheading_descriptions = request.POST.getlist('subheading_description')
        subheading_images = request.FILES.getlist('subheading_image')

        # Filter out empty subcontent entries
        filtered_subcontents = [
            (name, desc, img) for name, desc, img in zip(subheading_names, subheading_descriptions, subheading_images)
            if name.strip() or desc.strip() or img
        ]

        # Update existing sub-contents
        for index, sub_content in enumerate(sub_contents):
            if index < len(filtered_subcontents):
                name, desc, img = filtered_subcontents[index]
                Sub_Content.update(
                    sub_content.id,
                    cntntheading=content_to_update,
                    sb_heding=name,
                    sbcntnt=desc,
                    sbcontntImg=img if img else None
                )
            else:
                sub_content.delete()  # Delete extra sub-contents

        # Add new sub-contents if needed
        for index in range(len(sub_contents), len(filtered_subcontents)):
            name, desc, img = filtered_subcontents[index]
            Sub_Content.add(
                content_to_update,
                name,
                desc,
                img if img else None
            )

        return redirect('content_list')

    jsonData = json.dumps(data, indent=4)  # Serialize data for debugging or front-end use
    return render(request, "dashboard/edit-content.html", {
        'sections': sections,
        'pages': pages,
        'content_to_update': content_to_update,
        'sub_contents': sub_contents,
        'jsonData': jsonData
    })





def delete_content(request, content_id):
    sec_delete = get_object_or_404(Content, id=content_id)

    sec_delete.delete()

    return redirect('/')


@login_required
def page_add(request):
    if request.method == "POST":
        result = Pages.add(
            request.POST.get('name'),
            request.POST.get('heading'),
            request.POST.get('content'),
            request.FILES['myfile'],
            request.POST.get('page_Title'),
            request.POST.get('Page_meta_description'),
            request.POST.get('Page_meta_keywords')
        )
        print("\n\n\nresult\n\n", result)
    return render(request, "dashboard/page-add.html")


def page_edit(request, page_id):
    page = get_object_or_404(Pages, pk=page_id)
    myfile = request.FILES.get('myfile', None)
    if request.method == "POST":
        result = Pages.update(
            page_id,
            request.POST.get('name'),
            request.POST.get('heading'),
            request.POST.get('content'),
            myfile,
            request.POST.get('page_Title'),
            request.POST.get('Page_meta_description'),
            request.POST.get('Page_meta_keywords')
        )
        print("\n\n\nresult\n\n", result)
    return render(request, "dashboard/page-edit.html", {'page': page})


def delete_page(request, page_id):
    sec_delete = get_object_or_404(Pages, id=page_id)

    sec_delete.delete()

    return redirect('/')



def help(request):
    
    return render(request, "dashboard/help.html")











