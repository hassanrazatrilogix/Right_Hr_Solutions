# Generated by Django 4.2.16 on 2024-12-16 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=1024)),
                ('country', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=20)),
                ('accept_terms_conditions', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('Admin', 'Admin'), ('User', 'User')], default='User', max_length=50)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=500)),
                ('comments', models.TextField(blank=True, null=True)),
                ('terms', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('comments', models.TextField(blank=True, null=True)),
                ('accepted_terms', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoriesList', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('pick_date', models.DateField()),
                ('pick_time', models.TimeField()),
                ('comments_questions', models.TextField(blank=True, null=True)),
                ('terms_accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ImageField(upload_to='services/icons/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('upload_documents', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('type', models.CharField(max_length=50)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontend.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BillingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
