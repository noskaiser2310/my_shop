# Generated by Django 5.0.9 on 2024-10-14 06:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0015_shippingaddress_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="shippingaddress",
            name="name",
        ),
        migrations.AddField(
            model_name="shippingaddress",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
