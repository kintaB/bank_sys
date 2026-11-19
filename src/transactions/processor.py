from datetime import datetime

from src.exceptions import (
    AccountClosedError,
    AccountFrozenError,
    DayTimeOperationError,
    InsufficientFundsError,
    InvalidOperationError,
)
from src.models import (
    AuditSeverity,
    Currencies,
    RiskLevel,
    TransactionDeclinedReason,
    TransactionStatus,
    TransactionType,
)


class TransactionProcessor:
    def __init__(self, bank, audit_log=None, risk_analyzer=None, external_fee_rate=0.02, max_retries=1):
        self.bank = bank
        self.audit_log = audit_log
        self.risk_analyzer = risk_analyzer
        self.external_fee_rate = external_fee_rate
        self.max_retries = max_retries
        self.errors = []
        self.history = []

    def process_queue(self, queue):
        items = queue.get_next()
        for transaction in items:
            self.process_one(transaction)

    def _log(self, message, severity, transaction_id=None):
        if self.audit_log is not None:
            self.audit_log.add(message, severity, transaction_id)

    def _find_client_id_by_account(self, account_number):
        for client_id in self.bank.clients:
            client = self.bank.clients[client_id]
            for number in client.accounts:
                if number == account_number:
                    return client_id
        return None

    def process_one(self, transaction):
        print('EXECUTE:', transaction.id, transaction.type.value)

        # validate BEFORE risk analysis and money moves
        try:
            transaction.validate()
        except InvalidOperationError as error:
            print('REJECTED (invalid):', transaction.id, error)
            self._log(str(error), AuditSeverity.ERROR, transaction.id)
            transaction.transaction_status = TransactionStatus.FAILED
            transaction.declined_reason = TransactionDeclinedReason.INVALID_OPERATION
            transaction.updated_at = datetime.now()
            self.history.append(transaction)
            return

        if self.risk_analyzer is not None:
            level, reasons = self.risk_analyzer.analyze(transaction)
            reason_text = ', '.join(reasons)

            if level == RiskLevel.MEDIUM:
                self._log('medium risk: ' + reason_text, AuditSeverity.WARNING, transaction.id)
                client_id = self._find_client_id_by_account(transaction.sender)
                if client_id is not None:
                    self.bank.mark_suspicious(client_id, reason_text)

            if level == RiskLevel.HIGH:
                print('REJECTED (high risk):', transaction.id, reason_text)
                self._log('blocked high risk: ' + reason_text, AuditSeverity.CRITICAL, transaction.id)
                transaction.transaction_status = TransactionStatus.REJECTED
                transaction.declined_reason = TransactionDeclinedReason.HIGH_RISK
                transaction.updated_at = datetime.now()
                client_id = self._find_client_id_by_account(transaction.sender)
                if client_id is not None:
                    self.bank.mark_suspicious(client_id, 'blocked: ' + reason_text)
                self.history.append(transaction)
                return

        attempts = 0
        last_error = None

        while attempts <= self.max_retries:
            attempts = attempts + 1
            try:
                self._execute(transaction)
                transaction.transaction_status = TransactionStatus.COMPLETED
                transaction.declined_reason = None
                transaction.updated_at = datetime.now()
                self._log('completed ok', AuditSeverity.INFO, transaction.id)
                print('DONE:', transaction.id)

                if self.risk_analyzer is not None:
                    if transaction.type == TransactionType.TRANSFER or transaction.type == TransactionType.EXTERNAL_TRANSFER:
                        self.risk_analyzer.remember_receiver(transaction.sender, transaction.receiver)

                self.history.append(transaction)
                return
            except Exception as error:
                last_error = str(error)
                self.errors.append(transaction.id + ': ' + last_error)
                self._log(last_error, AuditSeverity.ERROR, transaction.id)

        print('REJECTED (failed):', transaction.id, last_error)
        transaction.transaction_status = TransactionStatus.FAILED
        transaction.declined_reason = self._reason_from_error(last_error)
        transaction.updated_at = datetime.now()
        self.history.append(transaction)

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
        if 'insufficient' in message or 'Insufficient' in message:
            return TransactionDeclinedReason.INSUFFICIENT_FUNDS
        if 'disableb' in message or '00:00' in message:
            return TransactionDeclinedReason.INVALID_OPERATION
        return TransactionDeclinedReason.INVALID_OPERATION

    def _get_account(self, account_number):
        return self.bank.accounts[account_number]

    def _credit(self, account, amount):
        # uses account.deposit -> status, daytime, polymorphic rules
        account.deposit(amount)

    def _debit(self, account, amount):
        # uses account.withdraw -> status, daytime, savings/premium rules
        account.withdraw(amount)

    def _execute(self, transaction):
        if transaction.type == TransactionType.DEPOSIT:
            account = self._get_account(transaction.receiver)
            amount = self.convert(transaction.amount, transaction.currency, account.currency)
            self._credit(account, amount)
            return

        sender = self._get_account(transaction.sender)

        if transaction.type == TransactionType.WITHDRAWAL:
            amount = self.convert(transaction.amount, transaction.currency, sender.currency)
            total = amount + transaction.commission
            self._debit(sender, total)
            return

        if transaction.type == TransactionType.INVESTMENT:
            amount = self.convert(transaction.amount, transaction.currency, sender.currency)
            self._debit(sender, amount)
            return

        if transaction.type == TransactionType.TRANSFER or transaction.type == TransactionType.EXTERNAL_TRANSFER:
            receiver = self._get_account(transaction.receiver)

            pay = self.convert(transaction.amount, transaction.currency, sender.currency)
            total = pay + transaction.commission

            if transaction.type == TransactionType.EXTERNAL_TRANSFER:
                fee = pay * self.external_fee_rate
                transaction.commission = transaction.commission + fee
                total = total + fee

            self._debit(sender, total)
            receive = self.convert(transaction.amount, transaction.currency, receiver.currency)
            self._credit(receiver, receive)
            return

        raise InvalidOperationError('unknown type')
