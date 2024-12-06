from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User, Appointment, Order, Document


admin.site.register(Appointment)
admin.site.register(Order)

admin.site.register(User)
admin.site.register(Document)


