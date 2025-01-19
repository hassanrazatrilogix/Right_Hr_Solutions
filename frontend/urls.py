from django.urls import path,include
from . import views
from .views import cart, checkout ,logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.home_recent, name='home_recent'),
    path('about/', views.about, name='about'),
    path('about/', views.about_recent, name='about_recent'),
    path('apostille-services/', views.apostilleservices, name='apostille-services'),
    path('appoinment/', views.appointment, name='appoinment'),
    path('background-check/', views.backgroundcheck, name='background-check'),
    path('contact-us/', views.contact, name='contact-us'),
    path("newsletter-submission/", views.newsletter_submission, name="newsletter_submission"),
    path('cart/', cart, name='cart'),
    path('cart/<str:order_id>/', cart, name='cart_with_uuid'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/<str:order_id>/', views.checkout, name='checkout_with_uuid'),
    path('document-translation-service/', views.documenttranslationservice, name='document-translation-service'),
    path('faqs/', views.faqs, name='faqs'),
    path('fingerprinting-service/', views.fingerprintingservice, name='fingerprinting-service'),
    path('government/', views.government, name='government'),
    path('government/', views.government_recent, name='government_recent'),
    path('header/', views.header, name='header'),
    path('hrsolutions/', views.hrsolutions, name='hrsolutions'),
    path('hrsolutions/', views.hrsolutions_recent, name='hrsolutions_recent'),
    path('notarypublic-service/', views.notarypublicservice, name='notarypublic-service'),
    path('privacy-policy/', views.privacypolicy, name='privacy-policy'),
    path('terms-conditions/', views.termsconditions, name='terms-conditions'),
    path('professional-services/', views.professional_services, name='professional-services'),
    path('professional-services/', views.professional_services_recent, name='professional_services_recent'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('forget-password/', views.forgetpassword, name='forget-password'),
    path('confirm-password/<uidb64>/<token>/', views.confirmpassword, name='confirm-password'),
    path('thank-you/', views.thankyou, name='thank-you'),
    path('welcome/', views.welcome, name='welcome'),
    path('accounts/', include('allauth.urls')),

    path('download_order_files/<int:id>/', views.download_order_files, name='download_order_files')
]
