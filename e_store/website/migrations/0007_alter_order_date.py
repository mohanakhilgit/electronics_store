# Generated by Django 4.2 on 2023-05-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0006_alter_cart_date_alter_duplicatecart_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
