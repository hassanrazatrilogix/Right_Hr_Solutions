# Generated by Django 4.2.17 on 2025-01-22 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0005_appointment_id_alter_appointment_appointment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_id',
            field=models.CharField(editable=False, max_length=10, unique=True),
        ),
    ]
