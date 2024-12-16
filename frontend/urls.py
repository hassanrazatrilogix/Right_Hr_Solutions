from django.urls import path,include
from . import views
from .views import cart, checkout , service_list, service_create, service_update, service_delete

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('apostille-services/', views.apostilleservices, name='apostille-services'),
    path('appoinment/', views.appointment, name='appoinment'),
    path('background-check/', views.backgroundcheck, name='background-check'),
    path('contact-us/', views.contact, name='contact-us'),
    path('cart/', cart, name='cart'),
    path('cart/<str:order_id>/', cart, name='cart_with_uuid'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/<str:order_id>/', views.checkout, name='checkout_with_uuid'),
    path('document-translation-service/', views.documenttranslationservice, name='document-translation-service'),
    path('faqs/', views.faqs, name='faqs'),
    path('fingerprinting-service/', views.fingerprintingservice, name='fingerprinting-service'),
    path('government/', views.government, name='government'),
    path('header/', views.header, name='header'),
    path('hrsolutions/', views.hrsolutions, name='hrsolutions'),
    path('notarypublic-service/', views.notarypublicservice, name='notarypublic-service'),
    path('privacy-policy/', views.privacypolicy, name='privacy-policy'),
    path('terms-conditions/', views.termsconditions, name='terms-conditions'),
    path('professional-services/', views.professional_services, name='professional-services'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('forget-password/', views.forgetpassword, name='forget-password'),
    path('confirm-password/<uidb64>/<token>/', views.confirmpassword, name='confirm-password'),
    path('thank-you/', views.thankyou, name='thank-you'),
    path('home/', views.adminpanel, name='home'),
    path('accounts/', include('allauth.urls')),


    path('service/', service_list, name='service_list'),  
    path('create/', service_create, name='service_create'),  
    path('<int:pk>/update/', service_update, name='service_update'),  
    path('<int:pk>/delete/', service_delete, name='service_delete'),  
]
