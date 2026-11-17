from datetime import datetime

from src.models import TransactionDeclinedReason, TransactionStatus


class TransactionQueue:
    def __init__(self):
        self.transactions = []
        self.deferred = []

    def add(self, transaction, priority=0, deferred=False):
        transaction.priority = priority
        if deferred:
            self.deferred.append(transaction)
        else:
            self.transactions.append(transaction)

    def get_next(self):
        # return all items, highest priority first
        result = []

        while len(self.transactions) > 0:
            best_index = 0
            i = 1
            while i < len(self.transactions):
                if self.transactions[i].priority > self.transactions[best_index].priority:
                    best_index = i
                i = i + 1

            best = self.transactions.pop(best_index)
            result.append(best)

        return result

    def process_deferred(self):
        for transaction in self.deferred:
            self.transactions.append(transaction)
        self.deferred = []

    def cancel(self, transaction_id):
        i = 0
        while i < len(self.transactions):
            if self.transactions[i].id == transaction_id:
                tx = self.transactions.pop(i)
                tx.transaction_status = TransactionStatus.CANCELLED
                tx.declined_reason = TransactionDeclinedReason.CANCELLED
                tx.updated_at = datetime.now()
                return True
            i = i + 1

        i = 0
        while i < len(self.deferred):
            if self.deferred[i].id == transaction_id:
                tx = self.deferred.pop(i)
                tx.transaction_status = TransactionStatus.CANCELLED
                tx.declined_reason = TransactionDeclinedReason.CANCELLED
                tx.updated_at = datetime.now()
                return True
            i = i + 1

        return False
