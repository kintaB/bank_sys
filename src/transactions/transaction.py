import math
from datetime import datetime

from src.exceptions import InvalidOperationError
from src.models import TransactionStatus


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
        self.validate()

    def validate(self):
        # amount must be a real number > 0
        if not isinstance(self.amount, (float, int)) or isinstance(self.amount, bool):
            raise InvalidOperationError(f'Invalid amount: {self.amount}')
        if not math.isfinite(self.amount):
            raise InvalidOperationError(f'Invalid amount: {self.amount}')
        if self.amount <= 0:
            raise InvalidOperationError(f'Invalid amount: {self.amount}')

        # commission must be a real number >= 0
        if not isinstance(self.commission, (float, int)) or isinstance(self.commission, bool):
            raise InvalidOperationError(f'Invalid commission: {self.commission}')
        if not math.isfinite(self.commission):
            raise InvalidOperationError(f'Invalid commission: {self.commission}')
        if self.commission < 0:
            raise InvalidOperationError(f'Invalid commission: {self.commission}')

    def __str__(self):
        return (
            f'Transaction({self.id}, {self.type.value}, {self.amount} {self.currency.value}, '
            f'status={self.transaction_status.value})'
        )
