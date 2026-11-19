from abc import ABC, abstractmethod
from datetime import datetime
import math
import uuid
from src.models import ClientData, AccountStatus, Currencies
from src.exceptions import AccountFrozenError, DayTimeOperationError, InsufficientFundsError, AccountClosedError, InvalidOperationError

class AbstractAccount(ABC):
    def __init__(self, id: int, client_data: ClientData, _balance: float, account_status: AccountStatus):
        self.id = id 
        self.client_data = client_data
        self._balance = _balance
        self.account_status = account_status

    @abstractmethod
    def get_account_info(self):
        pass
    
    @abstractmethod
    def deposit(self, amount):
        pass
    
    @abstractmethod
    def withdraw(self, amount):
        pass

class BankAccount(AbstractAccount):

    def __init__(self, id, client_data, _balance, account_status, currency: Currencies):
        self.currency = currency
        super().__init__(id, client_data, _balance, account_status)
        self.validate_data()
        self.account_number = str(uuid.uuid4())[:8]
        print(f'its yours uuid{self.account_number}')

    def __str__(self):
        return f'BankAccount: {self.client_data.name},{self.client_data.surname},{self.account_number[-4:]},{self._balance},{self.account_status},{self.currency}'

    def validate_data(self):
        if not isinstance(self.account_status, AccountStatus):
            raise InvalidOperationError(f'Invalid account status: {self.account_status}')
        if not isinstance(self.currency, Currencies):
            raise InvalidOperationError(f'Invalid account currency: {self.currency}')
        # same number rules as operation amounts, but 0 is allowed
        self._ensure_number(self._balance, allow_zero=True)

    def _ensure_active(self):
        if self.account_status == AccountStatus.ACTIVE:
            return
        if self.account_status == AccountStatus.FROZEN:
            raise AccountFrozenError(f'account with id: {self.id} is frozen') 
        if self.account_status == AccountStatus.CLOSED:
            raise AccountClosedError(f'account with id: {self.id} is closed') 
        else: 
            raise InvalidOperationError(f'Something went wrong')
        

    def status_logger(self):
        print('smth')
        return self
    
    def get_account_info(self):
        account_info = {
            'id': self.id,
            'name': self.client_data.name,
            'surname': self.client_data.surname,
            'account_number': self.account_number[-4:],
            'balance': self._balance,
            'status': self.account_status,
            'currency': self.currency
        }
        return account_info

    def _ensure_number(self, value, allow_zero=False):
        if not isinstance(value, (float, int)) or isinstance(value, bool):
            raise InvalidOperationError(f'Invalid amount: {value}')
        if not math.isfinite(value):
            raise InvalidOperationError(f'Invalid amount: {value}')
        if allow_zero:
            if value < 0:
                raise InvalidOperationError(f'Invalid amount: {value}')
        else:
            if value <= 0:
                raise InvalidOperationError(f'Invalid amount: {value}')

    def _ensure_amount(self, amount):
        self._ensure_number(amount, allow_zero=False)
        
    def deposit(self, amount):
        self._ensure_daytime()
        self._ensure_active()
        self._ensure_amount(amount)
        self._balance += amount
        print('Operation complete')
        
    
    def withdraw(self, amount):
        self._ensure_daytime()
        self._ensure_active()
        self._ensure_amount(amount)
        if self._balance < amount:
            raise InsufficientFundsError(f'Insufficient Funds, deposit to continue operation')
        self._balance -= amount
        print('Operation complete')
    
    def _ensure_daytime(self):
        current_hour = datetime.now().hour
        if current_hour < 5:
            raise DayTimeOperationError('Operations are disableb from 0:00 to 05:00')
        