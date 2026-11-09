from src.accounts.base import BankAccount
from src.exceptions import AccountFrozenError, InsufficientFundsError, AccountClosedError, InvalidOperationError
    #TODO what does overdraft mean
class PremiumAccount(BankAccount):
    def __init__(self, id, client_data, guarded_balance, account_status, currency, min_balance: float, monthly_interest_rate: float):
        self.min_balance = min_balance
        self.monthly_interest_rate = monthly_interest_rate
        super().__init__(id, client_data, guarded_balance, account_status)
    
    def apply_monthly_interest(self):
        #TODO some hard logic
        pass

    def __str__(self):
        return f'SavingsAccount: {self.client_data},{self.guarded_balance},{self.account_status},{self.client_data.account_number[-4:]},{self.currency}'

    def get_account_info(self):
        # TODO create dict for returning object
        return self.client_data, self.id, self.guarded_balance, self.account_status

    
    def withdraw(self, amount): 
        if self.account_status == 'frozen':
            raise AccountFrozenError(f'account with {self.id} is frozen') 
        if self.account_status == 'closed':
            raise AccountClosedError(f'account with {self.id} is closed') 
        elif amount > 0:
            if self.guarded_balance < amount:
                raise InsufficientFundsError(f'Insufficient Funds, deposit to continue operation')
            else:
                self.guarded_balance -= amount
                print('withdraw complete')
        else:
            print('something went wrong')