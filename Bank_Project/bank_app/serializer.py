from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Account, Statement


class DepositSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=20,decimal_places=2)
    class Meta:
        model = Account
        fields = ["amount"]


class withdrawalSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=20,decimal_places=2)
    pin = serializers.IntegerField(write_only=True)
    class Meta:
        model = Account
        fields = ["amount","pin"]


class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields = "__all__"


class TransferModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "to_account",
            "from_account",
            "amount",
        ]  # Empty because we are not directly serializing the Account model

    from_account = serializers.CharField()
    to_account = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        from_account_number = data.get("from_account")
        to_account_number = data.get("to_account")
        amount = data.get("amount")

        # Validate that amount is positive
        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")

        # Check if accounts exist and are IBAN type
        from_account = get_object_or_404(Account, account_number=from_account_number)
        to_account = get_object_or_404(Account, account_number=to_account_number)

        if from_account == to_account:
            raise serializers.ValidationError("Both accounts can not be the same.")
        if not from_account or not to_account:
            raise serializers.ValidationError(
                "One or both account numbers are invalid."
            )

        if from_account.account_type != "IBAN" or to_account.account_type != "IBAN":
            raise serializers.ValidationError("Both accounts must be of type IBAN.")

        # Check if the sender has enough balance
        if from_account.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")
        
        return data
