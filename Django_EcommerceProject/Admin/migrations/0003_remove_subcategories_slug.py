# Generated by Django 4.1 on 2022-08-12 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0002_subcategories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategories',
            name='slug',
        ),
    ]
