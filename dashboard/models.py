from django.db import models
from django.conf import settings
Role_CHOICES = [
    ("ADMIN", "Admin"),
    ("STAFF", "Staff"),
]


class ServiceType(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='services/icons/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, related_name="services", default=1)  # default set to 1


    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="cart_items" 
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    service_name = models.CharField(max_length=255, blank=True) 
    service_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  

    def __str__(self):
        return f"{self.user.username} - {self.service.name}"

    def save(self, *args, **kwargs):

        if not self.service_name:
            self.service_name = self.service.name
        if not self.service_price:
            self.service_price = self.service.price
        super(Cart, self).save(*args, **kwargs)

    def total_price(self):
        """Calculate the total price for this cart item (price * quantity)."""
        return self.quantity * self.service_price