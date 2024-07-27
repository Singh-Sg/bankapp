# Generated by Django 5.0.7 on 2024-07-27 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bank_app", "0004_remove_statement_transaction_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="statement",
            name="statement_type",
            field=models.CharField(
                choices=[
                    ("transfer", "transfer"),
                    ("withdrawal", "withdrawal"),
                    ("deposit", "deposit"),
                ],
                default=1,
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]
