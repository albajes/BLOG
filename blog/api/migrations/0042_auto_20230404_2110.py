# Generated by Django 3.1.7 on 2023-04-04 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='profile',
            name='blogs',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.blog', verbose_name='Мои подписки'),
            preserve_default=False,
        ),
    ]
