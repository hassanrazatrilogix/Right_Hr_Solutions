# Generated by Django 4.2.17 on 2025-01-13 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_alter_sub_content_contentheading'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_section',
            name='sectionDescription',
            field=models.TextField(blank=True, null=True),
        ),
    ]
