from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from common.business_exceptions import (
    InsufficientBalanceException,
    AccountFrozenException,
    BusinessException,
    ReceiverAccountInactiveException
)

from accounts.models import Account
from .models import Transaction,Transfer
from .cache_service import CacheService
import logging

logger = logging.getLogger(__name__)








class TransactionService:

    @staticmethod
    @transaction.atomic
    def deposit(user, amount):
        """
        Deposit money into the authenticated user's account.
        """
        account = TransactionService._get_locked_account(user)


        logger.info(
            "Deposit started | Account=%s Amount=%s",
            account.account_number,
            amount,
        )

        

        account.balance = F("balance") + amount
        account.save(update_fields=["balance"])

        account.refresh_from_db()

        Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TransactionType.DEPOSIT,
            amount=amount,
            balance_after_transaction=account.balance,
        )

        logger.info(
            "Deposit successful | Account=%s Amount=%s NewBalance=%s",
            account.account_number,
            amount,
            account.balance,
        )

        CacheService.clear_transaction_history(
            user.id
        )

        return account
    
    
    
    @staticmethod
    @transaction.atomic
    def withdraw(user, amount):

        account = TransactionService._get_locked_account(user)

        logger.info(
            "Withdrawal requested | Account=%s Amount=%s",
            account.account_number,
            amount,
        )

        if account.status != Account.AccountStatus.ACTIVE:
            
            raise AccountFrozenException()

        if account.balance < amount:
            logger.warning(
                "Insufficient balance | Account=%s Requested=%s Balance=%s",
                account.account_number,
                amount,
                account.balance,
            )
            raise InsufficientBalanceException()

        account.balance = F("balance") - amount
        account.save(update_fields=["balance"])

        account.refresh_from_db()

        Transaction.objects.create(
            account=account,
            transaction_type=Transaction.TransactionType.WITHDRAW,
            amount=amount,
            balance_after_transaction=account.balance,
        )

        logger.info(
            "Withdrawal successful | Account=%s Amount=%s Balance=%s",
            account.account_number,
            amount,
            account.balance,
        )

        CacheService.clear_transaction_history(
            user.id
        )

        return account
    

    @staticmethod
    def _get_locked_account(user):
        """
        Fetch and lock the authenticated user's account.
        """
        return (
            Account.objects
            .select_for_update()
            .get(user=user)
        )


    
    @staticmethod
    def _lock_accounts(sender, receiver):
        """
        Lock sender and receiver accounts in ascending ID order
        to prevent deadlocks.
        """

        account_ids = sorted([sender.id, receiver.id])

        locked_accounts = (
            Account.objects
            .select_for_update()
            .filter(id__in=account_ids)
            .order_by("id")
        )

        account_map = {
            account.id: account
            for account in locked_accounts
        }

        return (
            account_map[sender.id],
            account_map[receiver.id],
        )
    

        
    @staticmethod
    @transaction.atomic
    def transfer(
        sender_user,
        receiver_account_number,
        amount,
    ):
        """
        Transfer funds from the authenticated user's account
        to another active account in a single atomic transaction.
        """
        try:

            sender = get_object_or_404(
                Account,
                user=sender_user,
            )

            receiver = get_object_or_404(
                Account,
                account_number=receiver_account_number,
            )

            logger.info(
                "Transfer initiated | From=%s To=%s Amount=%s",
                sender.account_number,
                receiver.account_number,
                amount,
            )

            if sender.id == receiver.id:

                logger.warning(
                    "Self-transfer attempted | Account=%s",
                    sender.account_number,
                )

                raise BusinessException(
                    "You cannot transfer money to your own account."
                )

            sender, receiver = TransactionService._lock_accounts(
                sender,
                receiver,
            )

            if sender.status != Account.AccountStatus.ACTIVE:

                logger.warning(
                    "Transfer blocked | Sender account frozen=%s",
                    sender.account_number,
                )
                
                raise AccountFrozenException()

            if receiver.status != Account.AccountStatus.ACTIVE:
                logger.warning(
                    "Transfer blocked | Receiver inactive=%s",
                    receiver.account_number,
                )
                raise ReceiverAccountInactiveException()
            
            if sender.balance < amount:
                logger.warning(
                    "Transfer failed due to insufficient balance | Sender=%s Requested=%s Available=%s",
                    sender.account_number,
                    amount,
                    sender.balance,
                )
                raise InsufficientBalanceException()

            logger.info(
                "Updating account balances | Sender=%s Receiver=%s",
                sender.account_number,
                receiver.account_number,
            )
            
            sender.balance = F("balance") - amount
            sender.save(update_fields=["balance"])

            receiver.balance = F("balance") + amount
            receiver.save(update_fields=["balance"])

            sender.refresh_from_db()
            receiver.refresh_from_db()

            transfer = Transfer.objects.create(
                sender_account=sender,
                receiver_account=receiver,
                amount=amount,
                )

            logger.info(
                "Transfer record created | Reference=%s",
                transfer.reference_number,
            )

            Transaction.objects.create(
                account=sender,
                transaction_type=Transaction.TransactionType.DEBIT,
                amount=amount,
                balance_after_transaction=sender.balance,
                )

            Transaction.objects.create(
            account=receiver,
            transaction_type=Transaction.TransactionType.CREDIT,
            amount=amount,
            balance_after_transaction=receiver.balance,)

            logger.info(
                "Transfer completed successfully | Ref=%s Amount=%s",
                transfer.reference_number,
                amount,
            )

            CacheService.clear_transaction_history(
                sender.user.id
            )

            CacheService.clear_transaction_history(
                receiver.user.id
            )

            return transfer

        except Exception:
            logger.exception(
                "unexcepted error during transfer"
            )

            raise