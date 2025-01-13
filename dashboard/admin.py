from django.contrib import admin
from dashboard.models import Service , Cart, ServiceType, Pages, Add_Section, Content, Sub_Content

admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Cart)
admin.site.register(Pages)
admin.site.register(Add_Section)
admin.site.register(Content)
admin.site.register(Sub_Content)

