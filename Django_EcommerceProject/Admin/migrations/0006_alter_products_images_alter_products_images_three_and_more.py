# Generated by Django 4.1 on 2022-08-13 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0005_alter_subcategories_subcategory_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='images',
            field=models.ImageField(upload_to='Products_Image'),
        ),
        migrations.AlterField(
            model_name='products',
            name='images_three',
            field=models.ImageField(null=True, upload_to='Products_Image'),
        ),
        migrations.AlterField(
            model_name='products',
            name='images_two',
            field=models.ImageField(null=True, upload_to='Products_Image'),
        ),
    ]