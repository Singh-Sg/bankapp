from django.db import models


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Account(models.Model):
    ACCOUNT_TYPES = (("savings", "Savings"), ("current", "Current"), ("IBAN", "IBAN"))

    pin = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ifsc = models.CharField(max_length=11)
    account_number = models.CharField(max_length=20, unique=True)
    branch_name = models.CharField(max_length=250)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    bank_address = models.CharField(max_length=225)

    def __str__(self):
        return f"Account of {self.user}: {self.account_number}"


class Statement(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="account"
    )
    date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Statement for {self.amount} on {self.date}"
