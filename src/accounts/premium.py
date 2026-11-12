from src.accounts.base import BankAccount
from src.exceptions import InvalidOperationError

class PremiumAccount(BankAccount):
    def __init__(self, id, client_data, _balance, account_status, currency, withdraw_limit: float, overdraft_limit: float, commission: float):
        self.withdraw_limit = withdraw_limit
        self.overdraft_limit = overdraft_limit
        self.commission = commission

        super().__init__(id, client_data, _balance, account_status, currency)

    def __str__(self):
        return (
            f'PremiumAccount: {self.client_data.name}, {self.client_data.surname}, ****{self.client_data.account_number[-4:]}, ' 
            f'balance={self._balance}, {self.currency}, '
            f'status={self.account_status} '
            f'limits: withdraw={self.withdraw_limit}, overdraft={self.overdraft_limit}, '
            f'comission={self.commission}'
        ) 
       
    def get_account_info(self):
        account_info = {
            'id': self.id,
            'name': self.client_data.name,
            'surname': self.client_data.surname,
            'account_number': self.client_data.account_number[-4:],
            'balance': self._balance,
            'status': self.account_status,
            'currency': self.currency
        }
        return account_info
    
    def withdraw(self, amount): 
        self._ensure_active()
        self._ensure_amount(amount)

        total = amount + self.commission # 300
        # a = 200 wl = 500
        if amount <= self.withdraw_limit and self._balance - total >= -self.overdraft_limit :
            self._balance -= total
        else:
            raise InvalidOperationError(f'Invalid operation')
