# Generated by Django 4.0.6 on 2022-07-17 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_productdiscount_rate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productdiscount',
            options={'ordering': ['-start_at', '-end_at'], 'verbose_name': 'Product discount', 'verbose_name_plural': 'Product discounts'},
        ),
    ]
