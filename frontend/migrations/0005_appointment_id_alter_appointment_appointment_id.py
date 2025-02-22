# Generated by Django 4.2.17 on 2025-01-22 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0004_alter_appointment_appointment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointment_id',
            field=models.CharField(editable=False, max_length=5, unique=True),
        ),
    ]
