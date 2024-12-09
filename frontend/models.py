from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from frontend.utils import UserManager
from django.contrib.postgres.fields import JSONField

Role_CHOICES = [
    ("ADMIN", "Admin"),
    ("STAFF", "Staff"),
]

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, blank=True , null=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=False)  

 
    password = models.CharField(max_length=255)

    company_name = models.CharField(max_length=255, blank=False)
    position = models.CharField(max_length=255, blank=False)

    address = models.CharField(max_length=1024, blank=False)
    country = models.CharField(max_length=255, blank=False)
    state = models.CharField(max_length=255, blank=False)
    zip_code = models.CharField(max_length=20, blank=False)


    accept_terms_conditions = models.BooleanField(default=False)

   
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('User', 'User')], default='User')

    objects = UserManager()

    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email


class Appointment(models.Model):

    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    comments = models.TextField(blank=True, null=True)
    terms = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment for {self.name} on {self.date} at {self.time}"


class Order(models.Model):
    categoriesList = models.CharField(max_length=50)  
    servicesList = models.CharField(max_length=100)  
    pick_date = models.DateField()
    pick_time = models.TimeField()
    comments_questions = models.TextField(blank=True, null=True)
    terms_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.categoriesList} - {self.servicesList}"


class Document(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    upload_documents = models.FileField(upload_to='documents/', blank=True, null=True)
    type = models.CharField(max_length=50)

    def __str__(self):
        return f"Document for Order #{self.order.id} - {self.type}"
