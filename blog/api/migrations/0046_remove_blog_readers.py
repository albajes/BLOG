# Generated by Django 3.1.7 on 2023-04-04 18:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_blog_readers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='readers',
        ),
    ]
