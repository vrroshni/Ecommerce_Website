# Generated by Django 4.1 on 2022-08-13 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0008_remove_products_images_remove_products_images_three_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategories',
            name='Subcategory_Image',
            field=models.FileField(default=True, upload_to='media/Subcategory_Image'),
        ),
    ]