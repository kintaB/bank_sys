from src.main import BankAccount, ClientData, AccountFrozenError, InsufficientFundsError

new_client = ClientData('John', 'Vandal')
new_client2 = ClientData('Andrey', 'Karchunovskiy')
new_account = BankAccount(1, new_client, 1000.0, 'active','KZT')
new_account2 = BankAccount(2, new_client, 0, 'frozen','RUB')
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