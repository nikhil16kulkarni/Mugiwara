# Generated by Django 5.0.2 on 2024-04-07 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0012_remove_paymentrequest_status_paymentrequest_otp_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentrequest",
            name="awaiting_internal_approval",
            field=models.BooleanField(default=False),
        ),
    ]
