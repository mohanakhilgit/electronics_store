# Generated by Django 4.2 on 2023-05-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_order_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="date",
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
