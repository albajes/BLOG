# Generated by Django 3.1.7 on 2023-03-26 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0027_auto_20230326_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='author',
        ),
        migrations.AlterField(
            model_name='blog',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
    ]
