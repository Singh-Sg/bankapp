# Generated by Django 5.0.7 on 2024-07-26 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank_app", "0002_account_bank_address_account_pin_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="statement",
            name="transaction_type",
            field=models.CharField(
                choices=[("credit", "Credit"), ("debit", "Debit")],
                default=1,
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="statement",
            name="account",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="account",
                to="bank_app.account",
            ),
        ),
    ]
