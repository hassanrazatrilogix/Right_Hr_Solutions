# Generated by Django 4.2.17 on 2025-01-15 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_alter_help_description_alter_help_heading'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the section title (e.g., General Questions)', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(help_text='Enter the FAQ heading', max_length=255)),
                ('description', models.TextField(help_text='Enter the FAQ description')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='dashboard.faqsection')),
            ],
        ),
    ]
