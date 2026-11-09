import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
# TODO sort out python run error
from src.accounts.base import BankAccount
from src.models import ClientData, AccountStatus, Currencies
from src.exceptions import AccountFrozenError, InsufficientFundsError

new_client = ClientData('John', 'Vandal')
new_client2 = ClientData('Andrey', 'Karchunovskiy')
new_account = BankAccount(1, new_client, 1000.0, AccountStatus.ACTIVE, Currencies.KZT)
new_account2 = BankAccount(2, new_client, 0, AccountStatus.FROZEN, Currencies.RUB)
new_account.deposit(34500)
new_account.withdraw(1790.123213)

try:
    new_account.withdraw(100000000000)
except InsufficientFundsError as e:
    print(e)
print(new_account)

try:
    new_account2.deposit(555)
except AccountFrozenError as e:
    print(e)