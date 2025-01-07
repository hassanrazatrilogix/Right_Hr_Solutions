from django.contrib import admin
from dashboard.models import Service , Cart, ServiceType

admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Cart)

