# Generated by Django 3.1.7 on 2023-03-25 17:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0022_remove_blog_authors'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
