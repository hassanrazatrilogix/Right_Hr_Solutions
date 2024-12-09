from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, and role.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Set the role to ADMIN by default
        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)




from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import reverse

def send_password_reset_email(user, email):
    subject = "Password Reset Request"
    thank_you_url = reverse('confirmpassword')
    message = f"Hello \n\nYou requested a password reset. Please click the link below to reset your password:\n{settings.SITE_URL}{thank_you_url}\n\nThank you!"
    
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])