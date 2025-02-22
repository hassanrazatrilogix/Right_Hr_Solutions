# Generated by Django 4.2.17 on 2025-01-15 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_hr_solutions_apsotille_section_section_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Help',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(help_text='Enter the heading for the item', max_length=255)),
                ('description', models.TextField(help_text='Enter the description that slides down when the heading is clicked')),
            ],
        ),
    ]
