from datetime import datetime

from src.accounts.premium import PremiumAccount
from src.models import (
    AccountStatus,
    Currencies,
    TransactionDeclinedReason,
    TransactionStatus,
    TransactionType,
)


class TransactionProcessor:
    def __init__(self, bank, external_fee_rate=0.02, max_retries=1):
        self.bank = bank
        self.external_fee_rate = external_fee_rate
        self.max_retries = max_retries
        self.errors = []

    def process_queue(self, queue):
        items = queue.get_next()
        for transaction in items:
            self.process_one(transaction)

    def process_one(self, transaction):
        attempts = 0
        last_error = None

        while attempts <= self.max_retries:
            attempts = attempts + 1
            try:
                self._execute(transaction)
                transaction.transaction_status = TransactionStatus.COMPLETED
                transaction.declined_reason = None
                transaction.updated_at = datetime.now()
                return
            except Exception as error:
                last_error = str(error)
                self.errors.append(transaction.id + ': ' + last_error)

        transaction.transaction_status = TransactionStatus.FAILED
        transaction.declined_reason = self._reason_from_error(last_error)
        transaction.updated_at = datetime.now()

    def convert(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount

        rates = {
            Currencies.USD: 1.0,
            Currencies.EUR: 1.1,
            Currencies.RUB: 0.01,
            Currencies.KZT: 0.002,
            Currencies.CNY: 0.14,
        }
        in_usd = amount * rates[from_currency]
        return in_usd / rates[to_currency]

    def _reason_from_error(self, message):
        if message is None:
            return TransactionDeclinedReason.INVALID_OPERATION
        if 'frozen' in message:
            return TransactionDeclinedReason.ACCOUNT_FROZEN
        if 'closed' in message:
            return TransactionDeclinedReason.ACCOUNT_CLOSED
        if 'insufficient' in message:
            return TransactionDeclinedReason.INSUFFICIENT_FUNDS
        return TransactionDeclinedReason.INVALID_OPERATION

    def _get_account(self, account_number):
        return self.bank.accounts[account_number]

    def _check_active(self, account):
        if account.account_status == AccountStatus.FROZEN:
            raise ValueError('account is frozen')
        if account.account_status == AccountStatus.CLOSED:
            raise ValueError('account is closed')

    def _can_pay(self, account, total):
        if account._balance >= total:
            return True
        if isinstance(account, PremiumAccount):
            return account._balance - total >= -account.overdraft_limit
        return False

    def _execute(self, transaction):
        if transaction.type == TransactionType.DEPOSIT:
            account = self._get_account(transaction.receiver)
            self._check_active(account)
            amount = self.convert(transaction.amount, transaction.currency, account.currency)
            account._balance = account._balance + amount
            return

        sender = self._get_account(transaction.sender)
        self._check_active(sender)

        if transaction.type == TransactionType.WITHDRAWAL:
            amount = self.convert(transaction.amount, transaction.currency, sender.currency)
            total = amount + transaction.commission
            if not self._can_pay(sender, total):
                raise ValueError('insufficient funds')
            sender._balance = sender._balance - total
            return

        if transaction.type == TransactionType.INVESTMENT:
            amount = self.convert(transaction.amount, transaction.currency, sender.currency)
            if not self._can_pay(sender, amount):
                raise ValueError('insufficient funds')
            sender._balance = sender._balance - amount
            return

        if transaction.type == TransactionType.TRANSFER or transaction.type == TransactionType.EXTERNAL_TRANSFER:
            receiver = self._get_account(transaction.receiver)
            self._check_active(receiver)

            pay = self.convert(transaction.amount, transaction.currency, sender.currency)
            total = pay + transaction.commission

            if transaction.type == TransactionType.EXTERNAL_TRANSFER:
                fee = pay * self.external_fee_rate
                transaction.commission = transaction.commission + fee
                total = total + fee

            if not self._can_pay(sender, total):
                raise ValueError('insufficient funds')

            sender._balance = sender._balance - total
            receive = self.convert(transaction.amount, transaction.currency, receiver.currency)
            receiver._balance = receiver._balance + receive
            return

        raise ValueError('unknown type')
