from rest_framework import serializers
from .models import Account,Statement

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['balance','pin']
        # read_only_fields = ['id', 'date']

class withdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['balance','pin']

class StatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fiels = ['amount','balance']

class TransferModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["to_account","from_account","amount"]  # Empty because we are not directly serializing the Account model

    from_account = serializers.CharField()
    to_account = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        from_account_number = data.get('from_account')
        to_account_number = data.get('to_account')
        amount = data.get('amount')

        # Validate that amount is positive
        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")

        # Check if accounts exist and are IBAN type
        from_account = Account.objects.filter(account_number=from_account_number).first()
        to_account = Account.objects.filter(account_number=to_account_number).first()

        if from_account == to_account:
            raise serializers.ValidationError("Both accounts can not be the same.")
        if not from_account or not to_account:
            raise serializers.ValidationError("One or both account numbers are invalid.")

        if from_account.account_type != 'IBAN' or to_account.account_type != 'IBAN':
            raise serializers.ValidationError("Both accounts must be of type IBAN.")

        # Check if the sender has enough balance
        if from_account.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")

        return data