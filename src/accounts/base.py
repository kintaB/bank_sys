from abc import ABC, abstractmethod
import uuid
from src.models import ClientData
from src.exceptions import AccountFrozenError, InsufficientFundsError, AccountClosedError, InvalidOperationError

class AbstractAccount(ABC):
    def __init__(self, id: int, client_data: ClientData, guarded_balance: float, account_status: ('active', 'frozen', 'closed')):
        self.id = id 
        self.client_data = client_data
        self.guarded_balance = guarded_balance
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
        
# TODO what is логические статусы и запрет операций при неверных статусах
# TODO add limits, probably limits on payment(переводы)
# TODO add operation commision
class BankAccount(AbstractAccount):

    def __init__(self, id, client_data, guarded_balance, account_status, currency: ('RUB', 'USD', 'EUR', 'KZT', 'CNY')):
        self.currency = currency
        super().__init__(id, client_data, guarded_balance, account_status)
        if self.client_data.account_number is None or self.client_data.account_number == '' :
            client_uuid = uuid.uuid1()
            self.client_data.account_number = str(client_uuid)
            print(f'its yours uuid{client_uuid}')
        

    def __str__(self):
        return f'BankAccount: {self.client_data},{self.guarded_balance},{self.account_status},{self.client_data.account_number[-4:]},{self.currency}'

    def validate_client_data(client_data):
        # future logic
        return client_data

    def status_logger(self):
        print('smth')
        return self
    
    def get_account_info(self):
        # TODO create dict for returning object
        return self.client_data, self.id, self.guarded_balance, self.account_status
    
    def deposit(self, amount):
        if self.account_status == 'frozen':
            raise AccountFrozenError(f'account with {self.id} is frozen') 
        if self.account_status == 'closed':
            raise AccountClosedError(f'account with {self.id} is closed') 
        elif amount < 0:
            raise InvalidOperationError(f'You doing something wrong')
        elif amount > 0:
            self.guarded_balance += amount
            print('amount added')
        else:
            print('something went wrong')
    
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