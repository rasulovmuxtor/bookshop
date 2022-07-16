# Generated by Django 4.0.6 on 2022-07-16 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='books.author', verbose_name='author'),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='books', to='books.category', verbose_name='category'),
        ),
        migrations.AlterUniqueTogether(
            name='bookrating',
            unique_together={('user', 'book')},
        ),
    ]