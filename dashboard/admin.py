from django.contrib import admin
from dashboard.models import Service , Cart, ServiceType, Home, Hr_Solutions, Professional_Services, Government, About_Us
from .models import FAQSection, FAQ, Home_Recent, Professional_Services_Recent, Government_Recent, About_Us_Recent, Hr_Solutions_Recent

admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Cart)
admin.site.register(Home)
admin.site.register(Hr_Solutions)
admin.site.register(Professional_Services)
admin.site.register(Government)
admin.site.register(About_Us)


admin.site.register(Home_Recent)
admin.site.register(Professional_Services_Recent)
admin.site.register(Government_Recent)
admin.site.register(About_Us_Recent)
admin.site.register(Hr_Solutions_Recent)


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1

@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [FAQInline]

