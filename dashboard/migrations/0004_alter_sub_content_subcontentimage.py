# Generated by Django 4.2.17 on 2025-01-12 09:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_sub_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_content',
            name='subContentImage',
            field=models.FileField(upload_to='services/icons/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'svg', 'png', 'jpeg', 'jpg'])]),
        ),
    ]
