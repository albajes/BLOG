# Generated by Django 3.1.7 on 2023-03-30 10:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0033_auto_20230328_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='authors',
            field=models.ManyToManyField(blank=True, related_name='author_blog', to=settings.AUTH_USER_MODEL, verbose_name='Авторы'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='api.Tags', verbose_name='Теги'),
        ),
    ]
