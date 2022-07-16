# Generated by Django 4.0.6 on 2022-07-16 11:41

import autoslug.fields
import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('full_name', models.CharField(max_length=128, verbose_name='full name')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('slug', autoslug.fields.AutoSlugField(editable=True, populate_from='title', unique=True)),
                ('description', ckeditor.fields.RichTextField(verbose_name='description')),
                ('image', models.ImageField(upload_to='books/images/', verbose_name='image')),
                ('published_year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2099)], verbose_name='published year')),
                ('rating', models.FloatField(editable=False, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating')),
                ('total_in_stock', models.PositiveIntegerField(default=0, verbose_name='total in stock')),
                ('price', models.IntegerField(verbose_name='Price')),
                ('discount_price', models.IntegerField(default=0, verbose_name='discount price')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='products.author', verbose_name='author')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='products.category', verbose_name='category')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='BookRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating')),
                ('comment', models.TextField(blank=True, verbose_name='comment')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book', to='products.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Book Rating',
                'verbose_name_plural': 'Book Rating',
                'unique_together': {('user', 'book')},
            },
        ),
    ]