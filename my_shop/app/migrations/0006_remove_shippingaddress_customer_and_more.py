# Generated by Django 5.0.9 on 2024-10-12 15:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_alter_account_date_joined_alter_account_last_login_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="shippingaddress",
            name="customer",
        ),
        migrations.RemoveField(
            model_name="order",
            name="customer",
        ),
        migrations.AddField(
            model_name="order",
            name="account",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.account",
            ),
        ),
        migrations.AddField(
            model_name="shippingaddress",
            name="Account",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.account",
            ),
        ),
        migrations.DeleteModel(
            name="Customer",
        ),
    ]
