
from .models import User
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to authenticate using their email address
    instead of the username.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            else:
                print("Incorrect password")
                return None
        except User.DoesNotExist:
            print(f"No user found with email: {email}")
            return None
