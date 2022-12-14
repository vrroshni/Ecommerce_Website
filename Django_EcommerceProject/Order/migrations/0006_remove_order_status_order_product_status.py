# Generated by Django 4.0.7 on 2022-08-23 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0005_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='status',
        ),
        migrations.AddField(
            model_name='order_product',
            name='status',
            field=models.CharField(choices=[('Order Confirmed', 'Order Confirmed'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Order Confirmed', max_length=100, null=True),
        ),
    ]
