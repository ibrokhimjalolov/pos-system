# Generated by Django 5.0.2 on 2024-03-23 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pos_system", "0001_initial"),
        ("users", "0002_company_user_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="company",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="users.company",
            ),
        ),
        migrations.AddField(
            model_name="consumer",
            name="company",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="users.company",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="company",
            field=models.ForeignKey(
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="users.company",
            ),
        ),
    ]