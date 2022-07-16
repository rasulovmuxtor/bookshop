# Generated by Django 4.0.6 on 2022-07-16 14:43

import django.core.validators
from django.db import migrations, models
import user.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('security_code', models.CharField(max_length=6, verbose_name='security Code')),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+998991234567'.", regex='^\\+{1}998\\d{9}$')], verbose_name='phone number')),
                ('is_verified', models.BooleanField(default=False, verbose_name='verified')),
            ],
            options={
                'verbose_name': 'SMS Verification',
                'verbose_name_plural': 'SMS Verifications',
                'ordering': ('-modified_at',),
                'unique_together': {('security_code', 'phone_number')},
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.CharField(error_messages={'unique': 'A user with that phone number already exists.'}, max_length=13, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+998991234567'.", regex='^\\+{1}998\\d{9}$')], verbose_name='phone number')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('address', models.CharField(blank=True, max_length=150, verbose_name='address')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', user.manager.CustomUserManager()),
            ],
        ),
    ]
