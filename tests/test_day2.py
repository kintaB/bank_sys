import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.accounts.savings import SavingsAccount
from src.accounts.premium import PremiumAccount
from src.accounts.investment import InvestmentAccount
from src.models import ClientData, AccountStatus, Currencies, Assets
from src.exceptions import InvalidOperationError
# Savings
my_savings_acc_client = ClientData('Dmitriy', 'Saver') 
my_savings_acc = SavingsAccount(3, my_savings_acc_client, 300000, AccountStatus.ACTIVE, Currencies.EUR, 1000, 0.025)

print(my_savings_acc.get_account_info())
try:
    my_savings_acc.withdraw(16000)
except: 
    print('invalid withdraw ops')

try:
    my_savings_acc.withdraw(3000)
    print(my_savings_acc._balance)
except:
    print('invalid withdraw ops')    

my_savings_acc.apply_monthly_interest()
print(my_savings_acc.monthly_interest_rate)
print(my_savings_acc._balance)

# Premium
print(' ')
print('HERE IS A PREMIUM TESTS:')
print(' ')
my_premium_acc_client = ClientData('Alina', 'Luch')
my_premium_acc = PremiumAccount(4, my_premium_acc_client, 15000, AccountStatus.ACTIVE, Currencies.EUR, 500, 1000, 50)
my_premium_acc_2 = PremiumAccount(5, my_premium_acc_client, 1000, AccountStatus.ACTIVE, Currencies.RUB, 50000, 1000, 100)

print(my_premium_acc.get_account_info())
print(my_premium_acc._balance)

try:
    my_premium_acc.withdraw(2000)
except:
    print('wrong withdraw op')

try:
    my_premium_acc.withdraw(500)
    print(f'balance after withdraw 500 is {my_premium_acc._balance}')
except:
    print('invalid withdraw ops')

    
try:
    my_premium_acc_2.withdraw(1300)
    print(f'balance after using overdraft limit is {my_premium_acc_2._balance}')
except:
    print('invalid withdraw ops')


# Investment

print(' ')
print('HERE IS A Investment TESTS:')
print(' ')

my_invest_client = ClientData('Ivan', 'Investor')
my_invest_acc = InvestmentAccount(
    6,
    my_invest_client,
    10000,
    AccountStatus.ACTIVE,
    Currencies.USD,
    {'stocks': 0.0, 'bonds': 0.0, 'etf': 0.0},
)

print(my_invest_acc.get_account_info())

try:
    my_invest_acc.invest(20000, Assets.stocks)
except InvalidOperationError:
    print('invalid invest ops')

my_invest_acc.invest(3000, Assets.stocks)
my_invest_acc.invest(2000, Assets.bonds)
my_invest_acc.invest(1000, Assets.etf)
print(f'balance after invest is {my_invest_acc._balance}')
print(f'portfolio after invest is {my_invest_acc.portfolio}')

growth = my_invest_acc.project_yearly_growth({
    'stocks': 0.10,
    'bonds': 0.04,
    'etf': 0.07,
})
print(f'projected yearly growth is {growth}')

try:
    my_invest_acc.withdraw(500)
    print(f'balance after withdraw 500 is {my_invest_acc._balance}')
except InvalidOperationError:
    print('invalid withdraw ops')