from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from frontend.forms import ServiceForm , ServiceTypeForm
from dashboard.models import   Service,ServiceType, Cart
from frontend.models import Order
from django.shortcuts import  get_object_or_404
from frontend.forms import UserEditForm
from django.db.models import Q
from django.core.paginator import Paginator


@login_required(login_url='signin')
def adminpanel(request):
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
        
    return render(request, 'home.html', {'orders': orders_page})


@login_required(login_url='signin')
def user(request):
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

        if request.method                                                                                        == 'POST' and request.user.is_superuser:
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

        return render(request, 'user.html', {'users': users_page})

def edit_user(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    if not request.user.is_superuser:
        return redirect('user')  # Redirect if not a superuser

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user')  
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
    
    return render(request, "dashboard/pages.html")

def section_list(request):
    
    return render(request, "dashboard/section-list.html")

def section_add(request):
    
    return render(request, "dashboard/section-add.html")

def section_edit(request):
    
    return render(request, "dashboard/section-edit.html")


def content_list(request):
    
    return render(request, "dashboard/content-list.html")


def add_content(request):
    
    return render(request, "dashboard/add-content.html")

def edit_content(request):
    
    return render(request, "dashboard/edit-content.html")



def page_add(request):
    
    return render(request, "dashboard/page-add.html")


def page_edit(request):
    
    return render(request, "dashboard/page-edit.html")



def help(request):
    
    return render(request, "dashboard/help.html")













