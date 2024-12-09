from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('apostilleservices/', views.apostilleservices, name='apostilleservices'),
    path('appoinment/', views.appointment, name='appoinment'),
    path('backgroundcheck/', views.backgroundcheck, name='backgroundcheck'),
    path('checkout/', views.checkout, name='checkout'),
    path('contactus/', views.contactus, name='contactus'),
    path('documenttranslationservice/', views.documenttranslationservice, name='documenttranslationservice'),
    path('faqs/', views.faqs, name='faqs'),
    path('fingerprintingservice/', views.fingerprintingservice, name='fingerprintingservice'),
    path('government/', views.government, name='government'),
    path('header/', views.header, name='header'),
    path('hrsolutions/', views.hrsolutions, name='hrsolutions'),
    path('notarypublicservice/', views.notarypublicservice, name='notarypublicservice'),
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    path('professional_services/', views.professional_services, name='professional_services'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('confirmpassword/<uidb64>/<token>/', views.confirmpassword, name='confirmpassword'),
    path('thankyou/', views.thankyou, name='thankyou'),
]
