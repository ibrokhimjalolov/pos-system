# Generated by Django 5.0.2 on 2024-03-31 06:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pos_system", "0006_alter_orderproduct_original_price_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="count_in_box",
        ),
        migrations.RemoveField(
            model_name="product",
            name="price",
        ),
        migrations.RemoveField(
            model_name="product",
            name="stock_qty",
        ),
        migrations.RemoveField(
            model_name="product",
            name="unit",
        ),
    ]