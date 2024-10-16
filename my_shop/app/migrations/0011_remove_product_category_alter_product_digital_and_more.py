# Generated by Django 5.0.9 on 2024-10-13 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0010_alter_category_options_remove_category_parent_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="category",
        ),
        migrations.AlterField(
            model_name="product",
            name="digital",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.FloatField(),
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.ManyToManyField(related_name="product", to="app.category"),
        ),
    ]
