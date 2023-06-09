# Generated by Django 3.1.7 on 2023-03-25 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0020_auto_20230325_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='authors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to='auth.user'),
            preserve_default=False,
        ),
    ]
