from src.accounts.base import BankAccount
from src.accounts.premium import PremiumAccount
from src.accounts.savings import SavingsAccount
from src.audit import AuditLog, AuditReports, RiskAnalyzer
from src.bank import Bank, Client
from src.models import (
    AccountStatus,
    ClientData,
    ClientStatus,
    Currencies,
    TransactionStatus,
    TransactionType,
)
from src.transactions import Transaction, TransactionProcessor, TransactionQueue


class BankDemo:
    def __init__(self):
        self.bank = Bank()
        self.audit = AuditLog('logs/demo_audit.log')
        self.risk = RiskAnalyzer(large_amount=4000, frequent_limit=4)
        self.queue = TransactionQueue()
        self.processor = TransactionProcessor(self.bank, self.audit, self.risk)
        self.reports = AuditReports(self.audit, self.risk, self.processor)
        self.transactions = []
        self.balance_flow = []

    def setup(self):
        print('=== INIT BANK ===')
        names = [
            ('c1', 'John', 'Vandal', '111'),
            ('c2', 'Alina', 'Luch', '222'),
            ('c3', 'Ivan', 'Petrov', '333'),
            ('c4', 'Maria', 'Sidorova', '444'),
            ('c5', 'Omar', 'Ali', '555'),
            ('c6', 'Kate', 'Brown', '666'),
            ('c7', 'Leo', 'Kim', '777'),
        ]

        for client_id, name, surname, phone in names:
            client = Client(
                client_id,
                ClientData(name, surname),
                25,
                'pass',
                ClientStatus.ACTIVE,
                [],
                {'mail': name.lower() + '@mail.com', 'phone': phone, 'address': None},
            )
            self.bank.add_client(client)

        # 12 accounts
        a1 = BankAccount(1, ClientData('John', 'Vandal'), 8000, AccountStatus.ACTIVE, Currencies.USD)
        a2 = BankAccount(2, ClientData('John', 'Vandal'), 2000, AccountStatus.ACTIVE, Currencies.USD)
        a3 = PremiumAccount(3, ClientData('Alina', 'Luch'), 1500, AccountStatus.ACTIVE, Currencies.USD, 1000, 300, 10)
        a4 = BankAccount(4, ClientData('Alina', 'Luch'), 900, AccountStatus.ACTIVE, Currencies.USD)
        a5 = SavingsAccount(5, ClientData('Ivan', 'Petrov'), 5000, AccountStatus.ACTIVE, Currencies.USD, 100, 0.01)
        a6 = BankAccount(6, ClientData('Ivan', 'Petrov'), 1200, AccountStatus.ACTIVE, Currencies.USD)
        a7 = BankAccount(7, ClientData('Maria', 'Sidorova'), 3000, AccountStatus.ACTIVE, Currencies.USD)
        a8 = BankAccount(8, ClientData('Maria', 'Sidorova'), 700, AccountStatus.FROZEN, Currencies.USD)
        a9 = BankAccount(9, ClientData('Omar', 'Ali'), 4500, AccountStatus.ACTIVE, Currencies.USD)
        a10 = BankAccount(10, ClientData('Kate', 'Brown'), 2200, AccountStatus.ACTIVE, Currencies.USD)
        a11 = BankAccount(11, ClientData('Leo', 'Kim'), 1800, AccountStatus.ACTIVE, Currencies.USD)
        a12 = BankAccount(12, ClientData('Leo', 'Kim'), 400, AccountStatus.ACTIVE, Currencies.USD)

        self.bank.open_account('c1', a1)
        self.bank.open_account('c1', a2)
        self.bank.open_account('c2', a3)
        self.bank.open_account('c2', a4)
        self.bank.open_account('c3', a5)
        self.bank.open_account('c3', a6)
        self.bank.open_account('c4', a7)
        self.bank.open_account('c4', a8)  # frozen -> ops fail
        self.bank.open_account('c5', a9)
        self.bank.open_account('c6', a10)
        self.bank.open_account('c7', a11)
        self.bank.open_account('c7', a12)  # new receiver for senders who never transferred here

        self.acc = {
            'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'a6': a6,
            'a7': a7, 'a8': a8, 'a9': a9, 'a10': a10, 'a11': a11, 'a12': a12,
        }

        print('clients:', len(self.bank.clients))
        print('accounts:', len(self.bank.accounts))

    def _add_tx(self, tx, priority=0, deferred=False):
        print('QUEUE ADD:', tx.id, tx.type.value, 'priority=', priority, 'deferred=', deferred)
        self.queue.add(tx, priority=priority, deferred=deferred)
        self.transactions.append(tx)

    def run_simulation(self):
        print('=== SIMULATION (35 transactions) ===')
        a = self.acc

        # normal
        self._add_tx(Transaction('t01', TransactionType.DEPOSIT, 100, Currencies.USD, None, a['a1'].account_number), 1)
        self._add_tx(Transaction('t02', TransactionType.TRANSFER, 50, Currencies.USD, a['a1'].account_number, a['a4'].account_number), 2)
        self._add_tx(Transaction('t03', TransactionType.WITHDRAWAL, 80, Currencies.USD, a['a5'].account_number))
        self._add_tx(Transaction('t04', TransactionType.DEPOSIT, 200, Currencies.USD, None, a['a7'].account_number))
        self._add_tx(Transaction('t05', TransactionType.TRANSFER, 120, Currencies.USD, a['a9'].account_number, a['a10'].account_number))
        self._add_tx(Transaction('t06', TransactionType.EXTERNAL_TRANSFER, 40, Currencies.USD, a['a1'].account_number, a['a11'].account_number))
        self._add_tx(Transaction('t07', TransactionType.DEPOSIT, 60, Currencies.USD, None, a['a2'].account_number))
        self._add_tx(Transaction('t08', TransactionType.WITHDRAWAL, 30, Currencies.USD, a['a6'].account_number))
        self._add_tx(Transaction('t09', TransactionType.TRANSFER, 70, Currencies.USD, a['a3'].account_number, a['a4'].account_number))
        self._add_tx(Transaction('t10', TransactionType.INVESTMENT, 100, Currencies.USD, a['a5'].account_number))

        # more normal
        self._add_tx(Transaction('t11', TransactionType.DEPOSIT, 90, Currencies.USD, None, a['a9'].account_number))
        self._add_tx(Transaction('t12', TransactionType.TRANSFER, 25, Currencies.USD, a['a10'].account_number, a['a11'].account_number))
        self._add_tx(Transaction('t13', TransactionType.WITHDRAWAL, 15, Currencies.USD, a['a2'].account_number))
        self._add_tx(Transaction('t14', TransactionType.DEPOSIT, 110, Currencies.USD, None, a['a3'].account_number))
        self._add_tx(Transaction('t15', TransactionType.TRANSFER, 45, Currencies.USD, a['a7'].account_number, a['a4'].account_number))
        self._add_tx(Transaction('t16', TransactionType.WITHDRAWAL, 20, Currencies.USD, a['a11'].account_number))
        self._add_tx(Transaction('t17', TransactionType.DEPOSIT, 55, Currencies.USD, None, a['a6'].account_number))
        self._add_tx(Transaction('t18', TransactionType.TRANSFER, 35, Currencies.USD, a['a1'].account_number, a['a2'].account_number))
        self._add_tx(Transaction('t19', TransactionType.EXTERNAL_TRANSFER, 60, Currencies.USD, a['a9'].account_number, a['a7'].account_number))
        self._add_tx(Transaction('t20', TransactionType.DEPOSIT, 75, Currencies.USD, None, a['a10'].account_number))

        # failed / suspicious
        self._add_tx(Transaction('t21', TransactionType.WITHDRAWAL, 10, Currencies.USD, a['a8'].account_number))  # frozen
        self._add_tx(Transaction('t22', TransactionType.WITHDRAWAL, 999999, Currencies.USD, a['a2'].account_number))  # no money
        self._add_tx(Transaction('t23', TransactionType.WITHDRAWAL, 5000, Currencies.USD, a['a1'].account_number))  # large
        # large + first transfer to a12 => HIGH (blocked); receiver not remembered
        self._add_tx(Transaction('t25', TransactionType.TRANSFER, 4500, Currencies.USD, a['a1'].account_number, a['a12'].account_number))
        self._add_tx(Transaction('t24', TransactionType.TRANSFER, 150, Currencies.USD, a['a1'].account_number, a['a12'].account_number))  # still new if t25 blocked
        self._add_tx(Transaction('t26', TransactionType.WITHDRAWAL, 10, Currencies.USD, a['a1'].account_number))
        self._add_tx(Transaction('t27', TransactionType.WITHDRAWAL, 10, Currencies.USD, a['a1'].account_number))
        self._add_tx(Transaction('t28', TransactionType.WITHDRAWAL, 10, Currencies.USD, a['a1'].account_number))
        self._add_tx(Transaction('t29', TransactionType.DEPOSIT, 300, Currencies.USD, None, a['a5'].account_number))
        self._add_tx(Transaction('t30', TransactionType.TRANSFER, 80, Currencies.USD, a['a5'].account_number, a['a6'].account_number))

        self._add_tx(Transaction('t31', TransactionType.DEPOSIT, 40, Currencies.USD, None, a['a4'].account_number))
        self._add_tx(Transaction('t32', TransactionType.WITHDRAWAL, 25, Currencies.USD, a['a3'].account_number))
        self._add_tx(Transaction('t33', TransactionType.TRANSFER, 90, Currencies.USD, a['a9'].account_number, a['a10'].account_number))
        self._add_tx(Transaction('t34', TransactionType.EXTERNAL_TRANSFER, 30, Currencies.USD, a['a7'].account_number, a['a11'].account_number))
        self._add_tx(Transaction('t35', TransactionType.TRANSFER, 20, Currencies.USD, a['a11'].account_number, a['a12'].account_number), deferred=True)

        print('cancel deferred t35:', self.queue.cancel('t35'))

        self.balance_flow = [a['a1']._balance]
        items = self.queue.get_next()
        for tx in items:
            self.processor.process_one(tx)
            self.balance_flow.append(a['a1']._balance)

    def show_client_accounts(self, client_id):
        print('=== CLIENT ACCOUNTS', client_id, '===')
        client = self.bank.clients[client_id]
        for number in client.accounts:
            account = self.bank.accounts[number]
            print(number, account.account_status.value, account._balance, account.currency.value)

    def show_history(self):
        print('=== HISTORY ===')
        for tx in self.processor.history:
            print(tx, 'reason=', tx.declined_reason)

    def show_suspicious(self):
        print('=== SUSPICIOUS ===')
        for item in self.reports.suspicious_operations():
            print(item)

    def show_reports(self):
        print('=== REPORTS ===')
        ranking = self.bank.get_clients_ranking()
        print('top-3 clients:')
        i = 0
        while i < 3 and i < len(ranking):
            print(ranking[i])
            i = i + 1

        completed = 0
        failed = 0
        rejected = 0
        cancelled = 0
        for tx in self.transactions:
            if tx.transaction_status == TransactionStatus.COMPLETED:
                completed = completed + 1
            elif tx.transaction_status == TransactionStatus.FAILED:
                failed = failed + 1
            elif tx.transaction_status == TransactionStatus.REJECTED:
                rejected = rejected + 1
            elif tx.transaction_status == TransactionStatus.CANCELLED:
                cancelled = cancelled + 1

        print('tx stats:', {
            'completed': completed,
            'failed': failed,
            'rejected': rejected,
            'cancelled': cancelled,
            'total': len(self.transactions),
        })
        print('bank total balance:', self.bank.get_bank_total_balance())
        print('error stats:', self.reports.error_statistics())

    def run(self):
        self.setup()
        self.run_simulation()
        self.show_client_accounts('c1')
        self.show_history()
        self.show_suspicious()
        self.show_reports()
        return self
