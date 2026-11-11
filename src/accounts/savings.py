from src.accounts.base import BankAccount
from src.exceptions import InvalidOperationError

class SavingsAccount(BankAccount):
    def __init__(self, id, client_data, _balance, account_status, currency, min_balance: float, monthly_interest_rate: float):
        self.min_balance = min_balance
        self.monthly_interest_rate = monthly_interest_rate
        super().__init__(id, client_data, _balance, account_status, currency)
        if self._balance < self.min_balance:
            raise InvalidOperationError(f'Initial balance can not be lower than minimum balance: {self.min_balance}')
    
    def apply_monthly_interest(self):
        self._balance += self._balance * self.monthly_interest_rate

    def __str__(self):
        return f'SavingsAccount: {self.client_data.name}, {self.client_data.surname}, {self.client_data.account_number[-4:]}, {self._balance}, {self.min_balance}, {self.account_status}, {self.currency}, {self.monthly_interest_rate}'

    def get_account_info(self):
        account_info = {
            'id': self.id,
            'name': self.client_data.name,
            'surname': self.client_data.surname,
            'account_number': self.client_data.account_number[-4:],
            'balance': self._balance,
            'status': self.account_status,
            'currency': self.currency,
            'min_balance': self.min_balance,
            'monthly_interest_rate': self.monthly_interest_rate
        }
        return account_info
    
    
    def withdraw(self, amount): 
        self._ensure_active()
        potential_balance = self._balance - amount
        if amount <= 0:
            raise InvalidOperationError(f'Invalid amount: {amount}')
        if potential_balance < self.min_balance:
            raise InvalidOperationError(f'Operation abort, balance can not be lower than minimum balance: {self.min_balance}')
        self._balance -= amount