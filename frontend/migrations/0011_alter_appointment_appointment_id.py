# Generated by Django 4.2.17 on 2025-01-22 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0010_alter_appointment_appointment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_id',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
