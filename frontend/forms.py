import re
from django import forms
from .models import User, Appointment, Order, ContactUs, BillingDetails
from dashboard.models import Service , ServiceType
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'company_name', 'position', 'address', 'country', 'state', 'zip_code', 'accept_terms_conditions']

    def clean_email(self):
        email = self.cleaned_data['email']
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # General email format validation
        if not re.match(email_regex, email):
            raise ValidationError("Enter a valid email address.")
        
        # Ensure email ends with '.com'
        if not email.endswith('.com'):
            raise ValidationError("Email domain must end with '.com'.")
        
        # Check for existing email in the database
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use. Please use a different email address.")
        
        return email


    def clean_password(self):
        password = self.cleaned_data['password']
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")
        
        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']

        if len(phone_number) < 10:
            raise ValidationError("Phone number must be at least 10 characters.")
        
        # Regular expression to match various phone number formats
        phone_regex = r'^\+?\d{1,3}?[-.\s]?(\(\d{1,4}\)|\d{1,4})[-.\s]?\d{1,9}([-.\s]?\d{1,9})*$'
        
        if not re.match(phone_regex, phone_number):
            raise ValidationError("Enter a valid phone number (10 to 15 digits, with optional international code).")
        
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserEditForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label='New Password'
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'company_name', 
            'position', 
            'address', 
            'country', 
            'state', 
            'zip_code', 
            'is_superuser'
        ]
        widgets = {
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data
    
    
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class SetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time', 'name', 'email', 'phone', 'address', 'comments', 'terms']

    def clean_email(self):
        email = self.cleaned_data['email']
       
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_regex, email):
            raise ValidationError("Enter a valid email address.")
   
        if not email.endswith('.com'):
            raise ValidationError("Email domain must end with '.com'.")
        
        if Appointment.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use. Please use a different email address.")
        
        return email   
         
    widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def clean_terms(self):
        terms = self.cleaned_data.get('terms')
        if not terms:
            raise forms.ValidationError("You must accept the terms and conditions.")
        return terms


class OrderForm(forms.ModelForm):
    category_price = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False, widget=forms.HiddenInput()
    )

    class Meta:
        model = Order
        fields = ['categoriesList', 'pick_date', 'pick_time', 'comments_questions', 'terms_accepted']
        widgets = {
            'pick_date': forms.DateInput(attrs={'type': 'date'}),
            'pick_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        categoriesList = cleaned_data.get('categoriesList')

        if categoriesList:
            try:
                service = Service.objects.get(id=categoriesList.id)
                cleaned_data['category_price'] = service.price
            except Service.DoesNotExist:
                raise forms.ValidationError("The selected service does not exist.")
        else:
            raise forms.ValidationError("You must select a service category.")

        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)
        order.price = self.cleaned_data.get('category_price', 0.00)

        if commit:
            order.save()

        return order


class BillingDetailsForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'country', 'state', 'zip_code']

class ContactUs(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'address', 'comments', 'accepted_terms']

    def clean_email(self):
        email = self.cleaned_data['email']
       
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'   
        
        if not re.match(email_regex, email):
            raise ValidationError("Enter a valid email address.")
        
        if not email.endswith('.com'):
            raise ValidationError("Email domain must end with .com")
        
        return email
    
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [ 'service_type','name',  'price','icon']
        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-control'}),
        } 

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ['name']       