# Generated by Django 4.1 on 2022-08-13 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0004_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategories',
            name='Subcategory_Image',
            field=models.ImageField(blank=True, upload_to='SubCategories_Images'),
        ),
    ]