import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.accounts.base import BankAccount
from src.audit import AuditLog, AuditReports, RiskAnalyzer
from src.bank import Bank, Client
from src.models import AccountStatus, AuditSeverity, ClientData, ClientStatus, Currencies, TransactionType
from src.transactions import Transaction, TransactionProcessor, TransactionQueue

bank = Bank()
bank.add_client(
    Client('c1', ClientData('John', 'Vandal'), 25, 'p1', ClientStatus.ACTIVE, [],
           {'mail': 'a@mail.com', 'phone': '111', 'address': None})
)
bank.add_client(
    Client('c2', ClientData('Alina', 'Luch'), 30, 'p2', ClientStatus.ACTIVE, [],
           {'mail': 'b@mail.com', 'phone': '222', 'address': None})
)

audit = AuditLog('logs/audit.log')
risk = RiskAnalyzer(large_amount=3000, frequent_limit=3)

acc_a = BankAccount(1, ClientData('John', 'Vandal'), 20000, AccountStatus.ACTIVE, Currencies.USD)
acc_b = BankAccount(2, ClientData('Alina', 'Luch'), 1000, AccountStatus.ACTIVE, Currencies.USD)
acc_new = BankAccount(3, ClientData('Alina', 'Luch'), 100, AccountStatus.ACTIVE, Currencies.USD)
acc_newer = BankAccount(4, ClientData('Alina', 'Luch'), 100, AccountStatus.ACTIVE, Currencies.USD)

bank.open_account('c1', acc_a)
bank.open_account('c2', acc_b)
bank.open_account('c2', acc_new)
bank.open_account('c2', acc_newer)

queue = TransactionQueue()
processor = TransactionProcessor(bank, audit_log=audit, risk_analyzer=risk)

txs = [
    Transaction('n1', TransactionType.DEPOSIT, 100, Currencies.USD, None, acc_a.account_number),
    Transaction('n2', TransactionType.TRANSFER, 50, Currencies.USD, acc_a.account_number, acc_b.account_number),
    Transaction('s1', TransactionType.WITHDRAWAL, 5000, Currencies.USD, acc_a.account_number),
    Transaction('s2', TransactionType.TRANSFER, 200, Currencies.USD, acc_a.account_number, acc_new.account_number),
    Transaction('s3', TransactionType.WITHDRAWAL, 10, Currencies.USD, acc_a.account_number),
    Transaction('s4', TransactionType.WITHDRAWAL, 10, Currencies.USD, acc_a.account_number),
    # large + brand-new receiver for this sender => HIGH and blocked
    Transaction('s5', TransactionType.TRANSFER, 4000, Currencies.USD, acc_a.account_number, acc_newer.account_number),
]

for tx in txs:
    queue.add(tx)

processor.process_queue(queue)
reports = AuditReports(audit, risk, processor)

print('--- results ---')
for tx in txs:
    print(tx, 'reason=', tx.declined_reason)

print('suspicious:', reports.suspicious_operations())
print('profile c1:', reports.client_risk_profile('c1', bank))
print('error stats:', reports.error_statistics())
print('warning logs:', len(audit.filter(severity=AuditSeverity.WARNING)))
print('critical logs:', len(audit.filter(severity=AuditSeverity.CRITICAL)))
