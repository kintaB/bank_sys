from datetime import datetime

from src.models import Currencies, TransactionStatus, TransactionType


class Transaction:
    def __init__(self, id, type, amount, currency, sender, receiver=None, commission=0.0):
        self.id = id
        self.type = type
        self.amount = amount
        self.currency = currency
        self.commission = commission
        self.sender = sender
        self.receiver = receiver
        self.priority = 0
        self.transaction_status = TransactionStatus.PENDING
        self.declined_reason = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        return (
            f'Transaction({self.id}, {self.type.value}, {self.amount} {self.currency.value}, '
            f'status={self.transaction_status.value})'
        )
