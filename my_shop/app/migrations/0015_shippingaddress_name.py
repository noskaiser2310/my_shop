# Generated by Django 5.0.9 on 2024-10-14 06:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0014_remove_shippingaddress_address_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="shippingaddress",
            name="name",
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
