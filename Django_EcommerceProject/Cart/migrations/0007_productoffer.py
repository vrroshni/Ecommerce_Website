# Generated by Django 4.0.7 on 2022-09-05 07:08

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0018_alter_products_productimage_three_and_more'),
        ('Cart', '0006_subcategoryoffer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productoffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.IntegerField(default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subcategory_category_offers', to='Admin.products')),
            ],
        ),
    ]