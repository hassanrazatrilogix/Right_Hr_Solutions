# Generated by Django 4.2.17 on 2025-01-15 12:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_about_us_help_businesses_build_high_performing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hr_solutions',
            name='apsotille_section_section_image',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='apsotille_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='background_check_section_images',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='background_check_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='document_notarization_section_image',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='document_notarization_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='document_translations_section_image',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='document_translations_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='fingerprint_services_section_image',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='hr_solutions',
            name='fingerprint_services_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='benifits_management_section_image',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='benifits_management_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='payroll_management_section_images',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='payroll_management_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='special_project_section_image',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='special_project_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='staffing_recruiting_section_image',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='staffing_recruiting_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='training_and_develop_section_image',
            field=models.ImageField(blank=True, null=True, upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
        migrations.AddField(
            model_name='professional_services',
            name='training_and_develop_section_title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]