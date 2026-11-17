import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.accounts.base import BankAccount
from src.accounts.premium import PremiumAccount
from src.bank import Bank, Client
from src.models import AccountStatus, ClientData, ClientStatus, Currencies, TransactionType
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

acc_a = BankAccount(1, ClientData('John', 'Vandal'), 5000, AccountStatus.ACTIVE, Currencies.USD)
acc_b = BankAccount(2, ClientData('Alina', 'Luch'), 1000, AccountStatus.ACTIVE, Currencies.USD)
acc_p = PremiumAccount(3, ClientData('John', 'Vandal'), 100, AccountStatus.ACTIVE, Currencies.USD, 500, 200, 5)
acc_f = BankAccount(4, ClientData('Alina', 'Luch'), 800, AccountStatus.FROZEN, Currencies.USD)

bank.open_account('c1', acc_a)
bank.open_account('c2', acc_b)
bank.open_account('c1', acc_p)
bank.open_account('c2', acc_f)

queue = TransactionQueue()
processor = TransactionProcessor(bank)

txs = [
    Transaction('t1', TransactionType.DEPOSIT, 200, Currencies.USD, None, acc_a.account_number),
    Transaction('t2', TransactionType.WITHDRAWAL, 100, Currencies.USD, acc_a.account_number),
    Transaction('t3', TransactionType.TRANSFER, 150, Currencies.USD, acc_a.account_number, acc_b.account_number),
    Transaction('t4', TransactionType.EXTERNAL_TRANSFER, 50, Currencies.USD, acc_a.account_number, acc_b.account_number),
    Transaction('t5', TransactionType.TRANSFER, 250, Currencies.USD, acc_p.account_number, acc_b.account_number),
    Transaction('t6', TransactionType.WITHDRAWAL, 10, Currencies.USD, acc_f.account_number),
    Transaction('t7', TransactionType.WITHDRAWAL, 999999, Currencies.USD, acc_a.account_number),
    Transaction('t8', TransactionType.DEPOSIT, 75, Currencies.USD, None, acc_b.account_number),
    Transaction('t9', TransactionType.INVESTMENT, 20, Currencies.USD, acc_a.account_number),
    Transaction('t10', TransactionType.TRANSFER, 30, Currencies.USD, acc_a.account_number, acc_b.account_number),
]

queue.add(txs[0], priority=1)
queue.add(txs[1], priority=0)
queue.add(txs[2], priority=2)
queue.add(txs[3])
queue.add(txs[4])
queue.add(txs[5])
queue.add(txs[6])
queue.add(txs[7])
queue.add(txs[8])
queue.add(txs[9], deferred=True)

print('cancel deferred t10:', queue.cancel('t10'))
processor.process_queue(queue)

print('--- results ---')
for tx in txs:
    print(tx)
print('balances:', acc_a._balance, acc_b._balance, acc_p._balance)
print('errors:', processor.errors)
