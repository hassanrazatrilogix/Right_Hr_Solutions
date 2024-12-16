import re
from django import forms
from .models import User, Appointment, Order, ContactUs, BillingDetails, Service
from django.core.exceptions import ValidationError


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'company_name', 'position', 'address', 'country', 'state', 'zip_code', 'accept_terms_conditions']

    def clean_email(self):
        email = self.cleaned_data['email']
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_regex, email):
            raise ValidationError("Enter a valid email address.")
        
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class SetPasswordForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time', 'name', 'email', 'phone', 'address', 'comments', 'terms']
        
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
    class Meta:
        model = Order
        fields = ['categoriesList', 'pick_date', 'pick_time', 'comments_questions', 'terms_accepted']
        widgets = {
            'pick_date': forms.DateInput(attrs={'type': 'date'}),
            'pick_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    category_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    def clean(self):
        cleaned_data = super().clean()
        selected_category = cleaned_data.get('categoriesList')

        if selected_category == 'Apostille Service':
            cleaned_data['category_price'] = 109.00
        elif selected_category == 'Background Check':
            cleaned_data['category_price'] = 100.00
        elif selected_category == 'Staffing & Recruitment':
            cleaned_data['category_price'] = 110.00
        elif selected_category == 'Training & Development':
            cleaned_data['category_price'] = 120.00
        else:
            cleaned_data['category_price'] = 0.00

        return cleaned_data


class BillingDetailsForm(forms.ModelForm):
    class Meta:
        model = BillingDetails
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'country', 'state', 'zip_code']

class ContactUs(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'phone', 'address', 'comments', 'accepted_terms']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'icon', 'price']       