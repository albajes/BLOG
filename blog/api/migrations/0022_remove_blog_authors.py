# Generated by Django 3.1.7 on 2023-03-25 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20230325_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='authors',
        ),
    ]
