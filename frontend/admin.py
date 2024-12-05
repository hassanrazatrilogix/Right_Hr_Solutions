from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import *


admin.site.register(Appointment)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'categoriesList', 'servicesList', 'document_type', 'number_of_documents', 'pick_date', 'pick_time']
    search_fields = ['categoriesList', 'servicesList']
    list_filter = ['pick_date']

admin.site.register(Order, OrderAdmin)

User = get_user_model()

# class CustomUserAdmin(UserAdmin):
#     form = UserRegistrationForm 
#     model = User 
#     list_display = ["email", "username"] 

admin.site.register(User)


