from datetime import datetime

from src.models import RiskLevel, TransactionType


class RiskAnalyzer:
    def __init__(self, large_amount=3000, frequent_limit=3):
        self.large_amount = large_amount
        self.frequent_limit = frequent_limit
        self.known_accounts = []
        self.ops_by_sender = {}
        self.last_results = []

    def register_account(self, account_number):
        if account_number not in self.known_accounts:
            self.known_accounts.append(account_number)

    def analyze(self, transaction):
        reasons = []
        points = 0

        sender = transaction.sender
        if sender is None:
            sender = transaction.receiver

        if transaction.amount >= self.large_amount:
            reasons.append('large amount')
            points = points + 2

        if datetime.now().hour < 5:
            reasons.append('night operation')
            points = points + 2

        if transaction.type == TransactionType.TRANSFER or transaction.type == TransactionType.EXTERNAL_TRANSFER:
            if transaction.receiver not in self.known_accounts:
                reasons.append('transfer to new account')
                points = points + 2

        if sender not in self.ops_by_sender:
            self.ops_by_sender[sender] = 0
        self.ops_by_sender[sender] = self.ops_by_sender[sender] + 1

        if self.ops_by_sender[sender] >= self.frequent_limit:
            reasons.append('frequent operations')
            points = points + 1

        if points >= 4:
            level = RiskLevel.HIGH
        elif points >= 2:
            level = RiskLevel.MEDIUM
        else:
            level = RiskLevel.LOW

        self.last_results.append({
            'transaction_id': transaction.id,
            'sender': sender,
            'level': level,
            'reasons': reasons,
        })
        return level, reasons
