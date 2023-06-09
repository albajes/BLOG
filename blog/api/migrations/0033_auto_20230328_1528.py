# Generated by Django 3.1.7 on 2023-03-28 11:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0032_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='authors',
            field=models.ManyToManyField(related_name='author_blog', to=settings.AUTH_USER_MODEL, verbose_name='Авторы'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_blog', to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
    ]
