'''
TODO Add this errors
 AccountFrozenError 
 AccountClosedError
 InvalidOperationError
 InsufficientFundsError
'''

class ClientData:
    name: str
    surname: str
    account_number: int


class AbstractAccount:
    def __init__(self, id: int, client_data: ClientData, guarded_balance: float, account_status: ('active', 'frozen', 'closed')):
        self.id = id 
        self.clien_data = client_data
        self.guarded_balance = guarded_balance
        self.account_status = account_status

    def get_account_info(self):
        # TODO create dict for returning object
        return self.client_data, self.id, self.guarded_balance, self.account_status
    
    def deposit(self, amount): 
        if amount > 0:
            self.guarded_balance += amount
            print('amount added')
    
    def withdraw(self, amount, guarded_balance): 
        if amount > 0 and guarded_balance >= amount:
            self.guarded_balance -= amount
            print('withdraw approve')
        
# TODO what is логические статусы и запрет операций при неверных статусах
class BankAccount(AbstractAccount):

    def __init__(self, currency: ('RUB', 'USD', 'EUR', 'KZT', 'CNY')):
        self.currency = currency

    def validate_client_data(client_data):
        # future logic
        return client_data

    def status_logger(self):
        print('smth')
        return self
    
    def generate_uuid(account_number: int):
        if account_number == 0:
            print('create uuid')
            

