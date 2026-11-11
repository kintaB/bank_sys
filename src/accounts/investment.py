from src.accounts.base import BankAccount
from src.models import Assets, Portfolio
from src.exceptions import InvalidOperationError, InsufficientFundsError

class InvestmentAccount(BankAccount):
    def __init__(self, id, client_data, _balance, account_status, currency, portfolio: Portfolio):
        self.portfolio = portfolio
        super().__init__(id, client_data, _balance, account_status, currency)

    def __str__(self):
        return (
            f'InvestmentAccount: {self.client_data.name}, {self.client_data.surname}, ****{self.client_data.account_number[-4:]}, ' 
            f'balance={self._balance}, {self.currency}, '
            f'status={self.account_status} '
        ) 
       
    def get_account_info(self):
        account_info = {
            'id': self.id,
            'name': self.client_data.name,
            'surname': self.client_data.surname,
            'account_number': self.client_data.account_number[-4:],
            'balance': self._balance,
            'status': self.account_status,
            'currency': self.currency,
            'portfolio': self.portfolio 
        }
        return account_info
    
    def withdraw(self, amount): 
        self._ensure_active()
        total = self._balance - amount

        if amount <= 0:
            raise InvalidOperationError(f'Invalid amount: {amount}')
        
        if total <= 0:
            raise InsufficientFundsError(f'InsufficientFundsError')

        self._balance -= amount

    def invest(self, amount, asset):
        if asset in Assets and amount > 0 and amount <= self._balance:
            self._balance -= amount
            self.portfolio[asset.value] += amount
               
        else:
            raise InvalidOperationError('something went wrong')

    '''
    growth_rates should look like dict
    assets = {
    'stocks' : '10% 0.1',
    'bonds' : '4% 0.04',
    'etf' : '7% 0.07'
    }
    '''
    def project_yearly_growth(self, growth_rates):
        stocks_growth = self.portfolio['stocks'] * growth_rates['stocks']
        bonds_growth = self.portfolio['bonds'] * growth_rates['bonds']
        etf_growth = self.portfolio['etf'] * growth_rates['etf']

        growths_info = {
            'stocks_growth': stocks_growth,
            'bonds_growth': bonds_growth,
            'etf_growth': etf_growth
        }

        return growths_info