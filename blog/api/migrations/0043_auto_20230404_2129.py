# Generated by Django 3.1.7 on 2023-04-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20230404_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='blogs',
        ),
        migrations.AddField(
            model_name='profile',
            name='blogs',
            field=models.ManyToManyField(blank=True, to='api.Blog', verbose_name='Мои подписки'),
        ),
    ]
