# Generated by Django 4.2.17 on 2025-01-25 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0012_document_number_of_document_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
