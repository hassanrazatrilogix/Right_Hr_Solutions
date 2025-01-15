from django.urls import path

from . import views
from dashboard.views import  service_list, service_create, service_update, service_delete

urlpatterns = [

    path('', views.dashboard_summary, name='summary'),
    path('orders/', views.all_orders, name='orders'),
    path('orders_id/<int:id>/', views.edit_orders, name='edit_orders'),
    path('user/', views.user, name='user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit-user'),
  

    path('service/', service_list, name='service_list'),  
    path('create/', service_create, name='service_create'),  
    path('<int:pk>/update/', service_update, name='service_update'),  
    path('<int:pk>/delete/', service_delete, name='service_delete'),  

    path('service-types/', views.service_type_list, name='service_type_list'),
    path('service-types/new/', views.service_type_create, name='service_type_create'),
    path('service-types/<int:pk>/edit/', views.service_type_edit, name='service_type_edit'),
    path('service-types/<int:pk>/delete/', views.service_type_delete, name='service_type_delete'),


    path("cart/add/<int:service_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/remove/<int:service_id>/", views.remove_from_cart, name="remove_from_cart"),


    #To Do
    path('edit_professional_services/<int:professional_id>', views.edit_professional_services, name='edit_professional_services'),
    path('edit_hr_solutions/<int:hr_solution_id>', views.edit_hr_solutions, name='edit_hr_solutions'),
    path('home_edit/<int:home_id>/', views.home_edit, name='home_edit'),
    path('edit_government/<int:government_id>/', views.edit_government, name='edit_government'),
    path('about_us/<int:about_us_id>/', views.edit_about_us, name='edit_about_us'),
    path('home_list', views.home_list, name='home_list'),

    
    path('help/', views.help_list, name='help_list'),
    path('help/add/', views.help_add, name='help_add'),  # Add View
    path('help/<int:pk>/edit/', views.help_edit, name='help_edit'),  # Edit View
    path('help/<int:pk>/delete/', views.help_delete, name='help_delete'),  # Delete View



    
]
