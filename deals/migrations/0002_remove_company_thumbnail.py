# Generated by Django 3.0.6 on 2020-08-06 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='thumbnail',
        ),
    ]
