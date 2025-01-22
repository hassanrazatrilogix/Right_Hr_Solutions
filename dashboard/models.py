from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings
Role_CHOICES = [
    ("ADMIN", "Admin"),
    ("STAFF", "Staff"),
]


def get_serializable_data(instance):
    """
    Returns a dictionary of all field values of the given instance
    in a JSON-serializable format.
    """
    data = {}
    for field in instance._meta.fields:
        if field.name == 'original_data':
            continue  # Skip the original_data field itself

        value = getattr(instance, field.name)

        # Handle non-serializable fields
        if hasattr(value, 'url'):  # For ImageFieldFile or FileField
            data[field.name] = value.url if value else None
        elif isinstance(value, (str, int, float, bool, type(None))):
            data[field.name] = value
        else:
            data[field.name] = str(value)  # Fallback to string conversion

    return data


class BaseModelWithOriginalData(models.Model):
    original_data = models.JSONField(default=dict, blank=True)

    def get_model_name(self):
        return self._meta.model_name

    def save(self, *args, **kwargs):
        # Capture original data dynamically
        if not self.pk and not self.original_data:
            self.original_data = get_serializable_data(self)
        super().save(*args, **kwargs)

    def reset_to_original(self):
        # Reset fields to original data
        if self.original_data:
            for field, value in self.original_data.items():
                field_obj = self._meta.get_field(field)

                # Handle FileField or ImageField
                if isinstance(field_obj, (models.FileField, models.ImageField)):
                    # Strip MEDIA_URL from the value if it exists
                    if value and value.startswith(settings.MEDIA_URL):
                        value = value[len(settings.MEDIA_URL):]
                
                setattr(self, field, value)
            self.save()

    class Meta:
        abstract = True


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


class Home(BaseModelWithOriginalData):
    # Hero Section
    pagename = models.CharField(max_length=255, null=True, blank=True, default="Home")
    hero_title = models.CharField(max_length=255)
    hero_des = models.TextField()
    hero_buttonImage = models.ImageField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Video Section
    video_section_title = models.CharField(max_length=255)
    video_section_des = models.TextField()
    video_button_text = models.FileField(upload_to='videos/')
    video_button_image = models.ImageField(upload_to='services/icons/',
                                           validators=[FileExtensionValidator(
                                               ['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True, default='')

    # Service Section - HR Solutions
    service_section_title = models.CharField(max_length=255)
    service_section_desc = models.TextField()

    # HR Solutions List
    hr_solutions_title = models.CharField(max_length=255)
    hr_solutions_desc = models.TextField()
    hr_solutions_buttonImage = models.ImageField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    benefits_management_title = models.CharField(max_length=255)
    benefits_management_description = models.TextField()
    benefits_management_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    payroll_management_title = models.CharField(max_length=255)
    payroll_management_description = models.TextField()
    payroll_management_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    special_projects_title = models.CharField(max_length=255)
    special_projects_description = models.TextField()
    special_projects_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    staffing_recruitment_title = models.CharField(max_length=255)
    staffing_recruitment_description = models.TextField()
    staffing_recruitment_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    training_development_title = models.CharField(max_length=255)
    training_development_description = models.TextField()
    training_development_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Service Section - Professional Services
    professional_services_section_title = models.CharField(max_length=255)
    professional_services_section_subtitle = models.TextField()
    professional_services_buttonImage = models.ImageField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Professional Services List
    apostille_services_title = models.CharField(max_length=255)
    apostille_services_description = models.TextField()
    apostille_services_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    background_checks_title = models.CharField(max_length=255)
    background_checks_description = models.TextField()
    background_checks_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    document_notarization_title = models.CharField(max_length=255)
    document_notarization_description = models.TextField()
    document_notarization_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    document_translation_title = models.CharField(max_length=255)
    document_translation_description = models.TextField()
    document_translation_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    fingerprinting_services_title = models.CharField(max_length=255)
    fingerprinting_services_description = models.TextField()
    fingerprinting_buttonImage = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])


    # Why Choose Section
    why_choose_section_title = models.CharField(max_length=255)
    why_choose_section_image = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    expert_hr_guidance_section_title = models.CharField(max_length=255)
    expert_hr_guidance_section_desc = models.TextField()
    expert_hr_guidance_section_images = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    efficiency_compliance_section_title = models.CharField(max_length=255)
    efficiency_compliance_section_desc = models.TextField()
    efficiency_compliance_section_image = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    costomized_solution_section_title = models.CharField(max_length=255)
    costomized_solution_section_desc = models.TextField()
    costomized_solution_section_image = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    customer_satisfaction_section_title = models.CharField(max_length=255)
    customer_satisfaction_section_desc = models.TextField()
    customer_satisfaction_section_image = models.FileField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Get Started Section
    get_started_section_title = models.CharField(max_length=255)
    get_started_section_desc = models.TextField()

    def __str__(self):
        return self.pagename



class Professional_Services(BaseModelWithOriginalData):
    # Hero Section
    pagename = models.CharField(max_length=255, null=True, blank=True)
    hero_title = models.CharField(max_length=255)
    hero_text = models.TextField()
    hero_button_image = models.ImageField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Video Section
    comprehensive_professional_services_title = models.CharField(max_length=255)
    comprehensive_professional_services_desc = models.TextField()

    # Service Section - HR Solutions
    apostille_services_title = models.CharField(max_length=255)
    apostille_services_desc = models.TextField()
    apostille_services_image = models.ImageField(upload_to='services/icons/', validators=[FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    apostille_services_cover = models.CharField(max_length=255)
    legalization_of_business = models.CharField(max_length=255)
    apostille_for_employment = models.CharField(max_length=255)
    support_with_multi_lingual = models.CharField(max_length=255)

    # HR Solutions List
    background_checks_title = models.CharField(max_length=255)
    background_checks_desc = models.TextField()
    background_checks_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    background_checks_include = models.CharField(max_length=255)
    criminal_history_checks = models.CharField(max_length=255)
    tax_compliance_and_reporting = models.CharField(max_length=255)
    employment_verification = models.CharField(max_length=255)

    # Service Section - Professional Services
    document_notarization_title = models.CharField(max_length=255)
    document_notarization_desc = models.TextField()
    document_notarization_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    our_notary_services_include = models.CharField(max_length=255)
    contract_notarization = models.CharField(max_length=255)
    legal_document_verification = models.CharField(max_length=255)
    business_agreement_notarization = models.CharField(max_length=255)

    # Professional Services List
    document_translation_services_title = models.CharField(max_length=255)
    document_translation_services_des = models.TextField()
    document_translation_services_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    translation_services_include = models.CharField(max_length=255)
    business_and_legal  = models.CharField(max_length=255)
    employment_contracts = models.CharField(max_length=255)
    multi_lingual_support_for = models.CharField(max_length=255)

    # Why Choose Section
    fingerprinting_service_title = models.CharField(max_length=255)
    fingerprinting_service_desc = models.TextField()
    fingerprinting_service_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    fingerprinting_services_include = models.CharField(max_length=255)
    live_scan  = models.CharField(max_length=255)
    FBI_FDLE_and_FINRA  = models.CharField(max_length=255)
    fingerprint_archiving = models.CharField(max_length=255)

    # Why Choose List
    hr_ervices_tailored_title = models.CharField(max_length=255)
    hr_ervices_tailored_title_description = models.TextField()
    benifits_management_section_title = models.CharField(max_length=255, null=True, blank=True)
    benifits_management_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    payroll_management_section_title = models.CharField(max_length=255, null=True, blank=True)
    payroll_management_section_images = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    special_project_section_title = models.CharField(max_length=255, null=True, blank=True)
    special_project_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    staffing_recruiting_section_title = models.CharField(max_length=255, null=True, blank=True)
    staffing_recruiting_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    training_and_develop_section_title = models.CharField(max_length=255, null=True, blank=True)
    training_and_develop_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)

    # Why Choose Section

    why_choose_section_title = models.CharField(max_length=255)
    why_choose_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    expert_hr_guidance_section_title = models.CharField(max_length=255)
    expert_hr_guidance_section_desc = models.TextField()
    expert_hr_guidance_section_images = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    efficiency_compliance_section_title = models.CharField(max_length=255)
    efficiency_compliance_section_desc = models.TextField()
    efficiency_compliance_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    costomized_solution_section_title = models.CharField(max_length=255)
    costomized_solution_section_desc = models.TextField()
    costomized_solution_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    customer_satisfaction_section_title = models.CharField(max_length=255)
    customer_satisfaction_section_desc = models.TextField()
    customer_satisfaction_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Get Started Section
    start_simplifying_your_business_title = models.CharField(max_length=255)
    start_simplifying_your_business_desc = models.TextField()

    def __str__(self):
        return self.pagename


class Hr_Solutions(BaseModelWithOriginalData):
    # Hero Section
    pagename = models.CharField(max_length=255, null=True, blank=True)
    hero_title = models.CharField(max_length=255)
    hero_text = models.TextField()
    hero_button_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Video Section
    comprehensive_professional_services_title = models.CharField(max_length=255)
    comprehensive_professional_services_desc = models.TextField()

    # Service Section - HR Solutions
    employee_benefits_management_title = models.CharField(max_length=255)
    employee_benefits_management_desc = models.TextField()
    employee_benefits_management_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    benefits_management_cover = models.CharField(max_length=255)
    health_insurance = models.CharField(max_length=255)
    paid_time_off  = models.CharField(max_length=255)
    employee_wellness = models.CharField(max_length=255)

    # HR Solutions List
    payroll_management_title = models.CharField(max_length=255)
    payroll_management_desc = models.TextField()
    payroll_management_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    payroll_services = models.CharField(max_length=255)
    accurate_payroll = models.CharField(max_length=255)
    tax_compliance_and_reporting = models.CharField(max_length=255)
    employment_compensation = models.CharField(max_length=255)

    # Service Section - Professional Services
    special_HR_project_title = models.CharField(max_length=255)
    special_HR_project_desc = models.TextField()
    special_HR_project_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    what_we_offer = models.CharField(max_length=255)
    employee_handbook = models.CharField(max_length=255)
    hR_policy_development = models.CharField(max_length=255)
    employee_engagement = models.CharField(max_length=255)

    # Professional Services List
    staffing_recruitment_title = models.CharField(max_length=255)
    staffing_recruitment_desc = models.TextField()
    staffing_recruitment_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    what_we_offer_staffing = models.CharField(max_length=255)
    comprehensive_candidate = models.CharField(max_length=255)
    talent_matching_based  = models.CharField(max_length=255)
    recruitment_for_both  = models.CharField(max_length=255)

    # Why Choose Section
    training_development_title = models.CharField(max_length=255)
    training_development_desc = models.TextField()
    training_development_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    our_training_programs_include = models.CharField(max_length=255)
    Leadership = models.CharField(max_length=255)
    compliance_and_regulatory = models.CharField(max_length=255)
    skills_training_for_it = models.CharField(max_length=255)

    # Why Choose List
    comprehensive_professional_title = models.CharField(max_length=255)
    comprehensive_professional_desc = models.TextField()
    apsotille_section_title = models.CharField(max_length=255, null=True, blank=True)
    apsotille_section_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    background_check_section_title = models.CharField(max_length=255, null=True, blank=True)
    background_check_section_images = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    document_notarization_section_title = models.CharField(max_length=255, null=True, blank=True)
    document_notarization_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    document_translations_section_title = models.CharField(max_length=255, null=True, blank=True)
    document_translations_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    fingerprint_services_section_title = models.CharField(max_length=255, null=True, blank=True)
    fingerprint_services_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    # Why Choose Section

    why_choose_section_title = models.CharField(max_length=255)
    why_choose_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    expert_hr_guidance_section_title = models.CharField(max_length=255)
    expert_hr_guidance_section_desc = models.TextField()
    expert_hr_guidance_section_images = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    efficiency_compliance_section_title = models.CharField(max_length=255)
    efficiency_compliance_section_desc = models.TextField()
    efficiency_compliance_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    costomized_solution_section_title = models.CharField(max_length=255)
    costomized_solution_section_desc = models.TextField()
    costomized_solution_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    customer_satisfaction_section_title = models.CharField(max_length=255)
    customer_satisfaction_section_desc = models.TextField()
    customer_satisfaction_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Get Started Section
    get_started_with_right_title  = models.CharField(max_length=255)
    get_started_with_right_desc = models.TextField()

    def __str__(self):
        return self.pagename


class Government(BaseModelWithOriginalData):
    # Hero Section
    pagename = models.CharField(max_length=255, null=True, blank=True)
    hero_title = models.CharField(max_length=255)
    hero_text = models.TextField()
    hero_button_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Video Section
    government_partnerships_title = models.CharField(max_length=255)
    government_partnerships_desc = models.TextField()

    # Service Section - HR Solutions
    our_commitment_to_government_title = models.CharField(max_length=255)
    our_commitment_to_government_desc = models.TextField()
    our_commitment_to_government_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    # HR Solutions List
    our_services_for_government_agencies_title = models.CharField(max_length=255)
    our_services_for_government_agencies_description = models.TextField()

    hr_solutions_title = models.CharField(max_length=255)
    hr_solutions_desc = models.TextField()
    hr_solutions_buttonImage = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    benefits_management_title = models.CharField(max_length=255)
    benefits_management_description = models.TextField()
    benefits_management_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    payroll_management_title = models.CharField(max_length=255)
    payroll_management_description = models.TextField()
    payroll_management_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    special_projects_title = models.CharField(max_length=255)
    special_projects_description = models.TextField()
    special_projects_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    staffing_recruitment_title = models.CharField(max_length=255)
    staffing_recruitment_description = models.TextField()
    staffing_recruitment_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    training_development_title = models.CharField(max_length=255)
    training_development_description = models.TextField()
    training_development_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Service Section - Professional Services
    professional_services_section_title = models.CharField(max_length=255)
    professional_services_section_subtitle = models.TextField()
    professional_services_buttonImage = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Professional Services List
    apostille_services_title = models.CharField(max_length=255)
    apostille_services_description = models.TextField()
    apostille_services_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    background_checks_title = models.CharField(max_length=255)
    background_checks_description = models.TextField()
    background_checks_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    document_notarization_title = models.CharField(max_length=255)
    document_notarization_description = models.TextField()
    document_notarization_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    document_translation_title = models.CharField(max_length=255)
    document_translation_description = models.TextField()
    document_translation_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    fingerprinting_services_title = models.CharField(max_length=255)
    fingerprinting_services_description = models.TextField()
    fingerprinting_buttonImage = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Why Choose Section
    why_choose_section_title = models.CharField(max_length=255)
    why_choose_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    expert_hr_guidance_section_title = models.CharField(max_length=255)
    expert_hr_guidance_section_desc = models.TextField()
    expert_hr_guidance_section_images = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    efficiency_compliance_section_title = models.CharField(max_length=255)
    efficiency_compliance_section_desc = models.TextField()
    efficiency_compliance_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    costomized_solution_section_title = models.CharField(max_length=255)
    costomized_solution_section_desc = models.TextField()
    costomized_solution_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    customer_satisfaction_section_title = models.CharField(max_length=255)
    customer_satisfaction_section_desc = models.TextField()
    customer_satisfaction_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Get Started Section
    government_partnerships_tit = models.CharField(max_length=255)
    government_partnerships_des = models.TextField()

    def __str__(self):
        return self.pagename


class About_Us(BaseModelWithOriginalData):
    # Hero Section

    hero_title = models.CharField(max_length=255)
    pagename = models.CharField(max_length=255)
    hero_text = models.TextField()
    hero_button_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Video Section
    about_right_HR_title = models.CharField(max_length=255)
    about_right_HR_desc = models.TextField()

    # Service Section - HR Solutions
    our_story_title = models.CharField(max_length=255)
    our_story_desc = models.TextField()
    our_story_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    disadvantaged_business_enterprises = models.CharField(max_length=255)
    certified_women_owned_business = models.CharField(max_length=255)
    office_of_supplier = models.CharField(max_length=255)
    broward_health = models.CharField(max_length=255)
    minority_women_business = models.CharField(max_length=255)
    the_school_board_of = models.CharField(max_length=255)
    the_school_board  = models.CharField(max_length=255)
    broward_college = models.CharField(max_length=255)

    # HR Solutions List
    our_mission_title = models.CharField(max_length=255)
    our_mission_desc = models.TextField()
    our_mission_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    providing_personalized_hr_services = models.CharField(max_length=255)
    promoting_diversity_inclusion_and_equal = models.CharField(max_length=255)
    building_strong_long_lasting_relationships = models.CharField(max_length=255)

    # our vision

    our_vision_title = models.CharField(max_length=255, null=True, blank=True)
    our_vision_desc = models.TextField(null=True, blank=True)
    our_vision_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    help_businesses_build_high_performing = models.CharField(max_length=255, null=True, blank=True)
    support_employees_professional_development = models.CharField(max_length=255, null=True, blank=True)
    simplify_hr_management_for_businesses = models.CharField(max_length=255, null=True, blank=True)

    # Why Choose Section

    why_choose_section_title = models.CharField(max_length=255)
    why_choose_section_image = models.ImageField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    expert_hr_guidance_section_title = models.CharField(max_length=255)
    expert_hr_guidance_section_desc = models.TextField()
    expert_hr_guidance_section_images = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    efficiency_compliance_section_title = models.CharField(max_length=255)
    efficiency_compliance_section_desc = models.TextField()
    efficiency_compliance_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    costomized_solution_section_title = models.CharField(max_length=255)
    costomized_solution_section_desc = models.TextField()
    costomized_solution_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    customer_satisfaction_section_title = models.CharField(max_length=255)
    customer_satisfaction_section_desc = models.TextField()
    customer_satisfaction_section_image = models.FileField(upload_to='services/icons/', validators=[
        FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])

    # Get Started Section
    lets_build_success_title = models.CharField(max_length=255)
    lets_build_success_desc = models.TextField()

    def __str__(self):
        return self.pagename

class Help(BaseModelWithOriginalData):
    heading = models.CharField(max_length=255, help_text="Enter help title")
    description = models.TextField(help_text="Enter help description")

    def __str__(self):
        return self.heading
    


class FAQSection(models.Model):
    title = models.CharField(max_length=255, help_text="Enter the section title (e.g., General Questions)")

    def __str__(self):
        return self.title


class FAQ(models.Model):
    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, related_name="faqs")
    heading = models.CharField(max_length=255, help_text="Enter the FAQ heading")
    description = models.TextField(help_text="Enter the FAQ description")

    
    def __str__(self) -> str:
        return f"{self.section.title} - {self.heading}"
<<<<<<< HEAD
=======



    # Hero Section

    # hero_title = models.CharField(max_length=255)
    # pagename = models.CharField(max_length=255)
    # hero_text = models.TextField()
    # hero_button_image = models.ImageField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    #
    # # Video Section
    # about_right_HR_title = models.CharField(max_length=255)
    # about_right_HR_desc = models.TextField()
    #
    # # Service Section - HR Solutions
    # our_story_title = models.CharField(max_length=255)
    # our_story_desc = models.TextField()
    # our_story_image = models.ImageField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    # disadvantaged_business_enterprises = models.CharField(max_length=255)
    # certified_women_owned_business = models.CharField(max_length=255)
    # office_of_supplier = models.CharField(max_length=255)
    # broward_health = models.CharField(max_length=255)
    # minority_women_business = models.CharField(max_length=255)
    # the_school_board_of = models.CharField(max_length=255)
    # the_school_board  = models.CharField(max_length=255)
    # broward_college = models.CharField(max_length=255)
    #
    # # HR Solutions List
    # our_mission_title = models.CharField(max_length=255)
    # our_mission_desc = models.TextField()
    # our_mission_image = models.ImageField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    # providing_personalized_hr_services = models.CharField(max_length=255)
    # promoting_diversity_inclusion_and_equal = models.CharField(max_length=255)
    # building_strong_long_lasting_relationships = models.CharField(max_length=255)
    #
    # # our vision
    #
    # our_vision_title = models.CharField(max_length=255, null=True, blank=True)
    # our_vision_desc = models.TextField(null=True, blank=True)
    # our_vision_image = models.ImageField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])], null=True, blank=True)
    # help_businesses_build_high_performing = models.CharField(max_length=255, null=True, blank=True)
    # support_employees_professional_development = models.CharField(max_length=255, null=True, blank=True)
    # simplify_hr_management_for_businesses = models.CharField(max_length=255, null=True, blank=True)
    #
    # # Why Choose Section
    #
    # why_choose_section_title = models.CharField(max_length=255)
    # why_choose_section_image = models.ImageField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    # expert_hr_guidance_section_title = models.CharField(max_length=255)
    # expert_hr_guidance_section_desc = models.TextField()
    # expert_hr_guidance_section_images = models.FileField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    # efficiency_compliance_section_title = models.CharField(max_length=255)
    # efficiency_compliance_section_desc = models.TextField()
    # efficiency_compliance_section_image = models.FileField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    # costomized_solution_section_title = models.CharField(max_length=255)
    # costomized_solution_section_desc = models.TextField()
    # costomized_solution_section_image = models.FileField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    # customer_satisfaction_section_title = models.CharField(max_length=255)
    # customer_satisfaction_section_desc = models.TextField()
    # customer_satisfaction_section_image = models.FileField(upload_to='services/icons/', validators=[
    #     FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])])
    #
    # # Get Started Section
    # lets_build_success_title = models.CharField(max_length=255)
    # lets_build_success_desc = models.TextField()
    #
    # def __str__(self):
    #     return self.pagename
>>>>>>> a95bf9e (All changes fix today 23/2025)
