from django.urls import path
from . import views
from dashboard.views import  service_list, service_create, service_update, service_delete

urlpatterns = [
 
    path('', views.adminpanel, name='home'),
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
    path('pages', views.pages, name='pages'),

    path('section-list', views.section_list, name='section_list'),
    path('section-add', views.section_add, name='section_add'),
    path('section-edit', views.section_edit, name='section_edit'),


    path('content-list', views.content_list, name='content_list'),
    path('add-content', views.add_content, name='add_content'),
    path('edit-content', views.edit_content, name='edit-content'),



    path('page-add', views.page_add, name='page-add'),
     path('page-edit', views.page_edit, name='page-edit'),

    path('help', views.help, name='help'),



    
]
