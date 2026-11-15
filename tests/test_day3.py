import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.accounts.base import BankAccount
from src.bank import Bank, Client
from src.exceptions import AuthentificateFailedError, TooManyAttemptsError, YoungClientError
from src.models import AccountStatus, ClientData, ClientStatus, Currencies

bank = Bank()

client_a = Client(
    id='c1',
    full_name=ClientData('John', 'Vandal'),
    age=25,
    _password='secret1',
    client_status=ClientStatus.ACTIVE,
    accounts=[],
    contacts={'mail': 'john@mail.com', 'phone': '111', 'address': None},
)
client_b = Client(
    id='c2',
    full_name=ClientData('Alina', 'Luch'),
    age=30,
    _password='secret2',
    client_status=ClientStatus.ACTIVE,
    accounts=[],
    contacts={'mail': 'alina@mail.com', 'phone': '222', 'address': 'Astana'},
)

bank.add_client(client_a)
bank.add_client(client_b)

try:
    bank.add_client(
        Client(
            id='c3',
            full_name=ClientData('Kid', 'Young'),
            age=16,
            _password='x',
            client_status=ClientStatus.ACTIVE,
            accounts=[],
            contacts={'mail': 'kid@mail.com', 'phone': '333', 'address': None},
        )
    )
except YoungClientError as e:
    print(e)

acc1 = BankAccount(1, ClientData('John', 'Vandal'), 1000.0, AccountStatus.ACTIVE, Currencies.KZT)
acc2 = BankAccount(2, ClientData('John', 'Vandal'), 500.0, AccountStatus.ACTIVE, Currencies.USD)
acc3 = BankAccount(3, ClientData('Alina', 'Luch'), 8000.0, AccountStatus.ACTIVE, Currencies.EUR)

bank.open_account('c1', acc1)
bank.open_account('c1', acc2)
bank.open_account('c2', acc3)

print('total c1:', bank.get_total_balance('c1'))
print('total c2:', bank.get_total_balance('c2'))
print('ranking:', bank.get_clients_ranking())

bank.authenticate_client('111', 'secret1', 'c1')
print('login ok for c1')

try:
    bank.authenticate_client('111', 'wrong', 'c1')
except AuthentificateFailedError as e:
    print(e)

try:
    bank.authenticate_client('111', 'wrong', 'c1')
except AuthentificateFailedError as e:
    print(e)

try:
    bank.authenticate_client('111', 'wrong', 'c1')
except TooManyAttemptsError as e:
    print(e)

print('suspicious c1:', client_a._susp_operations)

bank.freeze_account(acc3.account_number)
print('acc3 status:', acc3.account_status)

found = bank.search_accounts([acc1.account_number, 'missing'])
print('search found:', list(found.keys()))
