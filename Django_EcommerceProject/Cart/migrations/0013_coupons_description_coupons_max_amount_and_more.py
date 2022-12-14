# Generated by Django 4.0.7 on 2022-09-12 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Cart', '0012_alter_coupons_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupons',
            name='description',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='coupons',
            name='max_amount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='coupons',
            name='min_amount',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='CouponUsedUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('coupon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Cart.coupons')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
