# Generated by Django 5.0.2 on 2024-03-01 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_account_account_status_account_closed_on_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="closed_on",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]