import re
from django import forms
from .models import User, Appointment, Order, ContactUs, BillingDetails
from dashboard.models import Service, ServiceType, Home, Professional_Services, Hr_Solutions, Government, About_Us, Help, FAQ, FAQSection
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'company_name', 'position', 'address', 'country', 'state', 'zip_code', 'image', 'accept_terms_conditions']

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

    # Add confirm_email field

    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'placeholder': 'Choose an image'}),
        label='Image'
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'company_name',
            'position',
            'address',
            'country',
            'state',
            'zip_code',
            'image',
            'is_superuser'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Validate password match
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
        fields = ['categoriesList', 'pick_date', 'pick_time', 'order_status', 'terms_accepted']
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


class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = '__all__'
        exclude = ['pagename', 'original_data'] 
        labels = {
            # Hero Section
            'hero_title': 'Hero Title',
            'hero_des': 'Hero Description',
            'hero_buttonImage': 'Hero Image',
            
            # Video Section
            'video_section_title': 'Video Section Title',
            'video_section_des': 'Video Section Description',
            'video_button_text': 'Video Button Text File',
            'video_button_image': 'Video Button Image',
            
            # Service Section - HR Solutions
            'service_section_title': 'Service Section Title',
            'service_section_desc': 'Service Section Description',
            
            # HR Solutions List
            'hr_solutions_title': 'HR Solutions Title',
            'hr_solutions_desc': 'HR Solutions Description',
            'hr_solutions_buttonImage': 'HR Solutions Button Image',
            'benefits_management_title': 'Benefits Management Title',
            'benefits_management_description': 'Benefits Management Description',
            'benefits_management_buttonImage': 'Benefits Management Button Image',
            'payroll_management_title': 'Payroll Management Title',
            'payroll_management_description': 'Payroll Management Description',
            'payroll_management_buttonImage': 'Payroll Management Button Image',
            'special_projects_title': 'Special Projects Title',
            'special_projects_description': 'Special Projects Description',
            'special_projects_buttonImage': 'Special Projects Button Image',
            'staffing_recruitment_title': 'Staffing & Recruitment Title',
            'staffing_recruitment_description': 'Staffing & Recruitment Description',
            'staffing_recruitment_buttonImage': 'Staffing & Recruitment Button Image',
            'training_development_title': 'Training & Development Title',
            'training_development_description': 'Training & Development Description',
            'training_development_buttonImage': 'Training & Development Button Image',
            
            # Service Section - Professional Services
            'professional_services_section_title': 'Professional Services Section Title',
            'professional_services_section_subtitle': 'Professional Services Section Subtitle',
            'professional_services_buttonImage': 'Professional Services Button Image',
            
            # Professional Services List
            'apostille_services_title': 'Apostille Services Title',
            'apostille_services_description': 'Apostille Services Description',
            'apostille_services_buttonImage': 'Apostille Services Button Image',
            'background_checks_title': 'Background Checks Title',
            'background_checks_description': 'Background Checks Description',
            'background_checks_buttonImage': 'Background Checks Button Image',
            'document_notarization_title': 'Document Notarization Title',
            'document_notarization_description': 'Document Notarization Description',
            'document_notarization_buttonImage': 'Document Notarization Button Image',
            'document_translation_title': 'Document Translation Title',
            'document_translation_description': 'Document Translation Description',
            'document_translation_buttonImage': 'Document Translation Button Image',
            'fingerprinting_services_title': 'Fingerprinting Services Title',
            'fingerprinting_services_description': 'Fingerprinting Services Description',
            'fingerprinting_buttonImage': 'Fingerprinting Button Image',
            
            # Why Choose Section
            'why_choose_section_title': 'Why Choose Section Title',
            'why_choose_section_image': 'Why Choose Section Image',
            'expert_hr_guidance_section_title': 'Expert HR Guidance Section Title',
            'expert_hr_guidance_section_desc': 'Expert HR Guidance Section Description',
            'expert_hr_guidance_section_images': 'Expert HR Guidance Section Images',
            'efficiency_compliance_section_title': 'Efficiency & Compliance Section Title',
            'efficiency_compliance_section_desc': 'Efficiency & Compliance Section Description',
            'efficiency_compliance_section_image': 'Efficiency & Compliance Section Image',
            'costomized_solution_section_title': 'Customized Solution Section Title',
            'costomized_solution_section_desc': 'Customized Solution Section Description',
            'costomized_solution_section_image': 'Customized Solution Section Image',
            'customer_satisfaction_section_title': 'Customer Satisfaction Section Title',
            'customer_satisfaction_section_desc': 'Customer Satisfaction Section Description',
            'customer_satisfaction_section_image': 'Customer Satisfaction Section Image',
            
            # Get Started Section
            'get_started_section_title': 'Get Started Section Title',
            'get_started_section_desc': 'Get Started Section Description',
        }


class ProfessionalServicesForm(forms.ModelForm):
    class Meta:
        model = Professional_Services
        fields = '__all__'
        exclude = ['pagename']


class HRSolutionsForm(forms.ModelForm):
    class Meta:
        model = Hr_Solutions
        fields = '__all__'
        exclude = ['pagename']


class GovernmentForm(forms.ModelForm):
    class Meta:
        model = Government
        fields = '__all__'
        exclude = ['pagename']


class AboutUsForm(forms.ModelForm):
    class Meta:
        model = About_Us
        fields = '__all__'
        exclude = ['pagename']


class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ['heading', 'description']
        labels = {
            'heading': 'Heading',
            'description': 'Description',
        }


class FAQForm(forms.ModelForm):
    # This defines a custom field for 'description'
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,  # Height of the textarea (lines)
            'cols': 100,  # Width of the textarea (characters)
            'class': 'form-control',  # Adding Bootstrap class for styling
        })
    )

    class Meta:
        model = FAQ
        fields = ['section', 'heading', 'description']  # Include 'description' in the fields
        labels = {
            'section': 'Section',
            'heading': 'FAQ Heading',
        }


class FAQSectionForm(forms.ModelForm):
    class Meta:
        model = FAQSection
        fields = ['title']
        labels = {
            'title': 'Section Title',
        }

