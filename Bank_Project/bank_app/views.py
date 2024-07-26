from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Account, Statement
from .serializer import DepositSerializer, withdrawalSerializer, TransferModelSerializer
import logging

class DepositAPIView(APIView):
    def patch(self, request, account_number):
        # import pdb;pdb.set_trace()    
        account = get_object_or_404(Account, account_number)
        # account = Account.objects.get(account_number = account_number)
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['balance']
            if amount <= 0:
                return Response({'error': 'Deposit amount must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            
            old_balance = account.balance
            new_balance = old_balance + amount
            account.balance = new_balance
            account.save()

            # Create a statement for the deposit
            statement = Statement.objects.create(
                account=account,
                amount=amount,
                balance=new_balance
            )

            return Response({'success': f'Deposit of {amount} successful. New balance is {new_balance}'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class withdrawal(APIView):
    def post(self, request, account_number):
        account = get_object_or_404(Account,account_number = account_number)
        serializer = withdrawalSerializer(data=request.data)
        
        if serializer.is_valid():
            amount = serializer.validated_data['balance']
            pin = serializer.validated_data['pin']
            if account.pin != pin:
                return Response("incorrect pin")
            if amount <= 0 :
                return Response({'error': 'Withdrawal amount must be greater than zero.'}, status=status.HTTP_400_BAD_REQUEST)
            if amount > account.balance:
                return Response({'error': 'insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
            old_balance = account.balance
            new_balance = old_balance - amount
            account.balance = new_balance
            account.save()

            # Create a statement for the deposit
            statement = Statement.objects.create(
                account=account,
                amount=amount,
                balance=new_balance
            )
            return Response(Statement.objects.values().last())
            return Response({'success': f'Deposit of {amount} successful. New balance is {new_balance}'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# logger = logging.getLogger(__name__)
    
class MoneyTransferAPIView(APIView):
    def post(self, request):
        serializer = TransferModelSerializer(data=request.data)
        
        if serializer.is_valid():
            from_account_number = serializer.validated_data['from_account']
            to_account_number = serializer.validated_data['to_account']
            amount = serializer.validated_data['amount']

            from_account = Account.objects.get(account_number=from_account_number)
            to_account = Account.objects.get(account_number=to_account_number)

            # Perform the transfer
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            # Create statements
            Statement.objects.create(account=from_account, amount=-amount, balance=from_account.balance)
            Statement.objects.create(account=to_account, amount=amount, balance=to_account.balance)

            return Response({'success': f'Transfer of {amount} successful.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)