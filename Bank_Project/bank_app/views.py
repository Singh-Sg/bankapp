from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Account, Statement
from .serializer import (
    DepositSerializer,
    withdrawalSerializer,
    TransferModelSerializer,
    StatementSerializer,
)
import logging

# Set up logging for debugging and monitoring
logger = logging.getLogger(__name__)


class DepositAPIView(APIView):
    def patch(self, request, account_number):
        # Retrieve the account object using the provided account number
        account = get_object_or_404(Account, account_number=account_number)
        serializer = DepositSerializer(data=request.data)

        if serializer.is_valid():
            amount = serializer.validated_data["amount"]

            # Check if the deposit amount is positive
            if amount <= 0:
                logger.warning(f"Deposit amount {amount} is not greater than zero.")
                return Response(
                    {"error": "Deposit amount must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update the account balance
            old_balance = account.balance
            new_balance = old_balance + amount
            account.balance = new_balance
            account.save()

            # Create a statement for the deposit
            Statement.objects.create(
                account=account,
                amount=amount,
                balance=new_balance,
                statement_type="deposit",
            )

            logger.info(
                f"Deposit of {amount} successful. New balance is {new_balance}."
            )
            return Response(
                {
                    "success": f"Deposit of {amount} successful. New balance is {new_balance}"
                },
                status=status.HTTP_200_OK,
            )

        # Log and return errors if serializer is invalid
        logger.error(f"Deposit failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalAPIView(APIView):
    def patch(self, request, account_number):
        # Retrieve the account object using the provided account number
        account = get_object_or_404(Account, account_number=account_number)
        serializer = withdrawalSerializer(data=request.data)

        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            pin = serializer.validated_data["pin"]

            # Verify the provided PIN
            if account.pin != pin:
                logger.warning(f"Incorrect PIN provided for account {account_number}.")
                return Response("Incorrect PIN", status=status.HTTP_400_BAD_REQUEST)

            # Check if the withdrawal amount is positive
            if amount <= 0:
                logger.warning(f"Withdrawal amount {amount} is not greater than zero.")
                return Response(
                    {"error": "Withdrawal amount must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if sufficient balance is available
            if amount > account.balance:
                logger.warning(f"Insufficient balance for withdrawal of {amount}.")
                return Response(
                    {"error": "Insufficient balance"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update the account balance
            old_balance = account.balance
            new_balance = old_balance - amount
            account.balance = new_balance
            account.save()

            # Create a statement for the withdrawal
            Statement.objects.create(
                account=account,
                amount=-amount,
                balance=new_balance,
                statement_type="withdrawal",
            )

            logger.info(
                f"Withdrawal of {amount} successful. New balance is {new_balance}."
            )
            return Response(
                {
                    "success": f"Withdrawal of {amount} successful. New balance is {new_balance}"
                },
                status=status.HTTP_200_OK,
            )

        # Log and return errors if serializer is invalid
        logger.error(f"Withdrawal failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MoneyTransferAPIView(APIView):
    def post(self, request):
        # Deserialize request data
        serializer = TransferModelSerializer(data=request.data)

        if serializer.is_valid():
            from_account_number = serializer.validated_data["from_account"]
            to_account_number = serializer.validated_data["to_account"]
            amount = serializer.validated_data["amount"]

            # Retrieve both account objects
            from_account = get_object_or_404(
                Account, account_number=from_account_number
            )
            to_account = get_object_or_404(Account, account_number=to_account_number)

            # Check if the transfer amount is positive
            if amount <= 0:
                logger.warning(f"Transfer amount {amount} is not greater than zero.")
                return Response(
                    {"error": "Transfer amount must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if sufficient balance is available in the source account
            if amount > from_account.balance:
                logger.warning(f"Insufficient balance for transfer of {amount}.")
                return Response(
                    {"error": "Insufficient balance"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Perform the transfer between accounts
            from_account.balance -= amount
            to_account.balance += amount
            from_account.save()
            to_account.save()

            # Create statements for both accounts
            Statement.objects.create(
                account=from_account,
                amount=-amount,
                balance=from_account.balance,
                statement_type="transfer",
            )
            Statement.objects.create(
                account=to_account,
                amount=+amount,
                balance=to_account.balance,
                statement_type="transfer",
            )

            logger.info(
                f"Transfer of {amount} from account {from_account_number} to account {to_account_number} successful."
            )
            return Response(
                {"success": f"Transfer of {amount} successful."},
                status=status.HTTP_200_OK,
            )

        # Log and return errors if serializer is invalid
        logger.error(f"Transfer failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatementAPIView(APIView):
    def get(self, request, account_number):
        try:
            # Retrieve all statements for the specified account number
            statement_list = Statement.objects.filter(
                account__account_number=account_number
            )

            # Check if there are any statements for the account
            if not statement_list.exists():
                logger.warning(
                    f"No statements found for account number {account_number}."
                )
                return Response(
                    {"detail": "No statements found for this account number."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Serialize the statement data
            serializer = StatementSerializer(statement_list, many=True)

            logger.info(
                f"Retrieved {statement_list.count()} statements for account number {account_number}."
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Statement.DoesNotExist:
            # Handle the case where no statements are found
            logger.error(f"Account number {account_number} not found.")
            return Response(
                {"detail": "Account number not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            # Handle any other unexpected errors
            logger.error(f"An error occurred: {str(e)}")
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
