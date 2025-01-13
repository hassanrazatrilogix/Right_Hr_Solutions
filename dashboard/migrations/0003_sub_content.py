# Generated by Django 4.2.17 on 2025-01-11 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub_Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_contentHeading', models.CharField(blank=True, max_length=255, null=True)),
                ('subContent', models.TextField()),
                ('subContentImage', models.ImageField(upload_to='services/icons/')),
                ('contentHeading', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.content')),
            ],
        ),
    ]