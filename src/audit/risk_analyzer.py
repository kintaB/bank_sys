from datetime import datetime, timedelta

from src.models import RiskLevel, TransactionType


class RiskAnalyzer:
    def __init__(self, large_amount=3000, frequent_limit=3, frequent_window_seconds=60):
        self.large_amount = large_amount
        self.frequent_limit = frequent_limit
        self.frequent_window = timedelta(seconds=frequent_window_seconds)
        # sender -> list of operation times
        self.ops_times = {}
        # sender -> list of receivers already used
        self.receivers_by_sender = {}
        self.last_results = []

    def remember_receiver(self, sender, receiver):
        if sender is None or receiver is None:
            return
        if sender not in self.receivers_by_sender:
            self.receivers_by_sender[sender] = []
        if receiver not in self.receivers_by_sender[sender]:
            self.receivers_by_sender[sender].append(receiver)

    def analyze(self, transaction):
        reasons = []
        points = 0
        now = datetime.now()

        sender = transaction.sender
        if sender is None:
            sender = transaction.receiver

        if transaction.amount >= self.large_amount:
            reasons.append('large amount')
            points = points + 2

        if now.hour < 5:
            reasons.append('night operation')
            points = points + 2

        # new receiver ONLY for this sender
        if transaction.type == TransactionType.TRANSFER or transaction.type == TransactionType.EXTERNAL_TRANSFER:
            known = []
            if sender in self.receivers_by_sender:
                known = self.receivers_by_sender[sender]
            if transaction.receiver not in known:
                reasons.append('transfer to new account')
                points = points + 2

        # frequent ops inside time window
        if sender not in self.ops_times:
            self.ops_times[sender] = []
        self.ops_times[sender].append(now)

        recent = []
        for moment in self.ops_times[sender]:
            if now - moment <= self.frequent_window:
                recent.append(moment)
        self.ops_times[sender] = recent

        if len(recent) >= self.frequent_limit:
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
