from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    User,
    PermissionsMixin,
)
from django.utils.timezone import now
from dashboard.models import Service
from frontend.utils import UserManager

import uuid
import logging

logger = logging.getLogger(__name__)

Role_CHOICES = [
    ("ADMIN", "Admin"),
    ("STAFF", "Staff"),
]

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, blank=True , null=True)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30, blank=False)  

 
    password = models.CharField(max_length=255)

    company_name = models.CharField(max_length=255, blank=False)
    position = models.CharField(max_length=255, blank=False)

    address = models.CharField(max_length=1024, blank=False)
    country = models.CharField(max_length=255, blank=False)
    state = models.CharField(max_length=255, blank=False)
    zip_code = models.CharField(max_length=10, null=False, blank=False, default="00000")
    image = models.ImageField(upload_to='documents/', blank=True, null=True)

    accept_terms_conditions = models.BooleanField(default=False)

   
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('User', 'User')], default='User')
    date_joined = models.DateTimeField(default=now)
    
    objects = UserManager()

    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email


Appointment_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('rescheduled', 'Rescheduled'),
    ]


class Appointment(models.Model):
    appointment_id = models.CharField(max_length=5, unique=True)
    service = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=500)
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Appointment_CHOICES, default='scheduled', blank=True, null=True)
    terms = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            logger.debug("Generating new appointment_id")
            last_appointment = Appointment.objects.all().order_by('-id').first()
            if last_appointment:
                last_id = int(last_appointment.appointment_id)
                new_id = str(last_id + 1).zfill(5)
                logger.debug(f"Generated new ID: {new_id}")
                while Appointment.objects.filter(appointment_id=new_id).exists():
                    logger.debug(f"ID {new_id} already exists. Incrementing...")
                    last_id += 1
                    new_id = str(last_id).zfill(5)
                logger.debug(f"Unique ID found: {new_id}")
            else:
                new_id = '00001'
                logger.debug(f"First record. Assigning ID: {new_id}")
            self.appointment_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment {self.appointment_id}"


Order_CHOICES = [
    ("NOT_STARTED", "Not Started"),
    ("IN_PROGRESS", "In Progress"),
    ("COMPLETED", "Completed"),
]


class Order(models.Model):
    order_id = models.CharField(max_length=5, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoriesList = models.ForeignKey(Service, on_delete=models.CASCADE)   
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    pick_date = models.DateField()
    pick_time = models.TimeField()
    order_status = models.CharField(max_length=50, choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Not Started')
    terms_accepted = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        if not self.order_id:
            logger.debug("Generating new appointment_id")
            last_order = Order.objects.all().order_by('-id').first()
            if last_order:
                last_id = int(last_order.order_id)
                new_id = str(last_id + 1).zfill(5)
                logger.debug(f"Generated new ID: {new_id}")
                while Order.objects.filter(order_id=new_id).exists():
                    logger.debug(f"ID {new_id} already exists. Incrementing...")
                    last_id += 1
                    new_id = str(last_id).zfill(5)
                logger.debug(f"Unique ID found: {new_id}")
            else:
                new_id = '00001'
                logger.debug(f"First record. Assigning ID: {new_id}")
            self.order_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.categoriesList}"

    @classmethod
    def update(cls, id, usr=None, categorList=None, prce=None, pick_date=None, pick_time=None, order_stats=None, terms_accepted=None):
        ls = Order.objects.get(id=id)

        if ls:
            if usr != None and usr != ls.user.email:
                ls.user.email = usr
            if categorList:
                service_instance = Service.objects.get(name=categorList)
                ls.categoriesList = service_instance
            if prce != None and prce != ls.price:
                ls.price = prce
            if pick_date != None and pick_date != ls.pick_date:
                ls.pick_date = pick_date
            if pick_time != None and pick_time != ls.pick_time:
                ls.pick_time = pick_time
            if order_stats != None and order_stats != ls.order_status:
                ls.order_status = order_stats
            if terms_accepted != None and terms_accepted != ls.terms_accepted:
                ls.terms_accepted = terms_accepted
            ls.save()
            print(ls)
            return ls



class Document(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    upload_documents = models.FileField(upload_to='documents/', blank=True, null=True)
    type = models.CharField(max_length=50)
    number_of_document = models.CharField(max_length=50, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Document for Order #{self.order.id} - {self.type}"


class BillingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50) 
    zip_code = models.CharField(max_length=10)
    
    def __str__(self):
        return f"Checkout for {self.user.username}"


class ContactUs(models.Model):
    name = models.CharField(max_length=25)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    address=models.TextField()
    comments = models.TextField(blank=True, null=True)
    accepted_terms = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.email})"
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
    

    

